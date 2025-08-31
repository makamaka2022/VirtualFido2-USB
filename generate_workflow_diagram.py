#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FIDO2 Workflow Diagram Generator
Generates visual workflow diagrams for FIDO2 device authentication process
Based on the original 18-step workflow from readme.txt
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, ConnectionPatch
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import os
import matplotlib.font_manager as fm
import platform

def setup_chinese_font():
    """Setup Chinese font for matplotlib"""
    # Try to find a Chinese font
    chinese_fonts = ['SimHei', 'Microsoft YaHei', 'SimSun', 'KaiTi', 'FangSong', 'Arial Unicode MS']
    
    # Check system type
    system = platform.system()
    
    if system == "Windows":
        # Windows fonts
        font_paths = [
            "C:/Windows/Fonts/simhei.ttf",
            "C:/Windows/Fonts/msyh.ttc",
            "C:/Windows/Fonts/simsun.ttc",
            "C:/Windows/Fonts/simkai.ttf",
            "C:/Windows/Fonts/simfang.ttf"
        ]
        
        for font_path in font_paths:
            if os.path.exists(font_path):
                try:
                    fm.fontManager.addfont(font_path)
                    font_name = os.path.splitext(os.path.basename(font_path))[0]
                    plt.rcParams['font.sans-serif'] = [font_name] + plt.rcParams['font.sans-serif']
                    plt.rcParams['axes.unicode_minus'] = False
                    print(f"Using Chinese font: {font_name} from {font_path}")
                    return True
                except Exception as e:
                    print(f"Failed to load font {font_path}: {e}")
                    continue
    
    # Try font family names
    for font_name in chinese_fonts:
        try:
            font_path = fm.findfont(fm.FontProperties(family=font_name))
            if font_path != fm.rcParams['font.sans-serif']:
                plt.rcParams['font.sans-serif'] = [font_name] + plt.rcParams['font.sans-serif']
                plt.rcParams['axes.unicode_minus'] = False
                print(f"Using Chinese font: {font_name}")
                return True
        except:
            continue
    
    # If no Chinese font found, use default and warn
    print("Warning: No Chinese font found, Chinese text may not display correctly")
    return False

def create_fido2_workflow_diagram(language='en'):
    """
    Create FIDO2 workflow diagram as an image based on the original 18 steps
    
    Args:
        language (str): 'en' for English, 'zh' for Chinese
    """
    
    # Setup font for Chinese
    if language == 'zh':
        setup_chinese_font()
    
    # Set up the figure with more space for all 18 steps
    fig, ax = plt.subplots(1, 1, figsize=(20, 16))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 16)
    ax.axis('off')
    
    # Define colors
    colors = {
        'init': '#E3F2FD',      # Light blue for initialization
        'registration': '#F3E5F5',  # Light purple for registration
        'pin_setup': '#FFF3E0',     # Light orange for PIN setup
        'auth': '#E8F5E8',      # Light green for authentication
        'error': '#FFEBEE',     # Light red for errors
        'success': '#E8F5E8',  # Light green for success
        'border': '#1976D2'     # Dark blue for borders
    }
    
    # Define text based on language - following the exact 18 steps
    if language == 'zh':
        title = "FIDO2 设备工作流程（18步详细版）"
        steps = [
            "1. 设备初始化，创建CA的公钥、私钥和证书",
            "2. 创建生成凭据的公钥、私钥和基于CA证书的凭据证书",
            "3. 创建PIN通信的公钥私钥",
            "4. 客户端请求MakeCredential",
            "5. 设备检测是否支持PIN，若是则检测是否已经设置PIN",
            "6. 若未设置PIN，则返回错误码，告诉client需要设置PIN",
            "7. 客户端发送getKeyAgreement获取密钥交换信息，计算共享密钥",
            "8. 客户端使用共享密钥对用户输入密码进行加密，将加密后的密码和自己的公钥信息一并发送给设备",
            "9. 设备收到setPIN请求后，使用客户端发送过来的公钥信息生成共享密钥，使用共享密钥对加密过的PIN码进行解密，然后记录PIN码的hash值",
            "10. 客户端发送getPINToken请求，设备使用共享密钥对发送过来的加密过的pinHash进行解密，并与本地记录的pinHash进行对比验证，若匹配则返回使用共享密钥加密过的pinToken",
            "11. 这时设备已经完成了PIN码的设置和pinToken的获取，若设备不支持PIN，则没有6~10的步骤",
            "12. 继续接着步骤5，若设备支持PIN并且PIN已经设置，则根据客户端的请求对pinToken进行校验，如果pinToken校验失败，则返回PIN码错误信息",
            "13. 设备不支持PIN，或者pinToken校验成功后，设备开始创建凭证，创建凭证前设备会通过一定的方式弹出认证UI，让用户决定是否允许创建凭证",
            "14. 用户允许后，设备开始创建凭证信息并将凭证信息发送给客户端，然后本地存储一份。凭据信息包含证书、公钥和随机生成的凭据ID",
            "15. 客户端请求GetAssertion认证，设备根据客户端传递过来的凭据ID查找本地是否存在对应的凭据信息",
            "16. 若不存在，则返回凭据不存在的错误信息",
            "17. 若存在，则对token、rp等信息进行简单校验，然后将客户端传递过来的clientDataHash、rp信息和本地存储的凭据相关信息一并发送给客户端，并对这些数据进行签名",
            "18. 客户端收到设备发送的Assertion数据，使用设备的公钥进行校验，然后对发送过来的凭证信息进行对比认证"
        ]
    else:
        title = "FIDO2 Device Workflow (18-Step Detailed Version)"
        steps = [
            "1. Device initialization, create CA public key, private key, and certificate",
            "2. Create credential public key, private key and credential certificate based on CA certificate",
            "3. Create PIN communication public/private key pair",
            "4. Client requests MakeCredential",
            "5. Device checks if PIN is supported, if yes then checks if PIN is already set",
            "6. If PIN is not set, return error code, telling client PIN setup is required",
            "7. Client sends getKeyAgreement to get key exchange information, calculate shared key",
            "8. Client encrypts user input password with shared key, sends encrypted password and public key info to device",
            "9. Device receives setPIN request, uses client's public key to generate shared key, decrypts encrypted PIN with shared key, then records PIN hash value",
            "10. Client sends getPINToken request, device decrypts encrypted pinHash with shared key, compares with locally stored pinHash, if match returns shared key encrypted pinToken",
            "11. Device has completed PIN setup and pinToken acquisition, if device doesn't support PIN, steps 6-10 are skipped",
            "12. Continue from step 5, if device supports PIN and PIN is set, validate pinToken per client request, if validation fails return PIN error",
            "13. Device doesn't support PIN, or pinToken validation succeeds, device starts creating credential, before creating credential device shows authentication UI for user consent",
            "14. After user allows, device creates credential info and sends to client, then stores locally. Credential info includes certificate, public key, and randomly generated credential ID",
            "15. Client requests GetAssertion authentication, device looks up credential info by credential ID passed from client",
            "16. If not found, return credential not found error",
            "17. If found, validate token, rp info, then send clientDataHash, rp info from client and locally stored credential info to client, and sign this data",
            "18. Client receives Assertion data from device, verifies with device's public key, then compares received credential info for authentication"
        ]
    
    # Draw title
    ax.text(6, 15.5, title, fontsize=18, fontweight='bold', ha='center', va='center')
    
    # Draw the 18 steps in a logical flow
    y_start = 14
    step_height = 0.7
    
    # Phase 1: Initialization (Steps 1-3)
    ax.text(2, y_start + 0.5, "Phase 1: Device Initialization" if language == 'en' else "第一阶段：设备初始化", 
            fontsize=12, fontweight='bold', ha='center', va='center', color=colors['border'])
    
    for i in range(3):
        y = y_start - i * step_height
        box = FancyBboxPatch((0.5, y-0.25), 3, 0.5, 
                            boxstyle="round,pad=0.1", 
                            facecolor=colors['init'], 
                            edgecolor=colors['border'], 
                            linewidth=2)
        ax.add_patch(box)
        ax.text(2, y, steps[i], fontsize=9, ha='center', va='center', wrap=True)
    
    # Phase 2: Credential Registration Start (Step 4)
    ax.text(6, y_start + 0.5, "Phase 2: Credential Registration" if language == 'en' else "第二阶段：凭据注册", 
            fontsize=12, fontweight='bold', ha='center', va='center', color=colors['border'])
    
    y = y_start
    box = FancyBboxPatch((4.5, y-0.25), 3, 0.5, 
                        boxstyle="round,pad=0.1", 
                        facecolor=colors['registration'], 
                        edgecolor=colors['border'], 
                        linewidth=2)
    ax.add_patch(box)
    ax.text(6, y, steps[3], fontsize=9, ha='center', va='center', wrap=True)
    
    # Phase 3: PIN Support Check (Step 5)
    y = y_start - step_height
    box = FancyBboxPatch((4.5, y-0.25), 3, 0.5, 
                        boxstyle="round,pad=0.1", 
                        facecolor=colors['registration'], 
                        edgecolor=colors['border'], 
                        linewidth=2)
    ax.add_patch(box)
    ax.text(6, y, steps[4], fontsize=9, ha='center', va='center', wrap=True)
    
    # PIN Decision Branch
    y_pin = y_start - 2 * step_height
    ax.text(6, y_pin, "PIN Support Decision" if language == 'en' else "PIN支持决策", 
            fontsize=10, fontweight='bold', ha='center', va='center')
    
    # PIN Not Set Branch (Step 6)
    y_pin_not_set = y_pin - step_height
    box = FancyBboxPatch((1.5, y_pin_not_set-0.25), 3, 0.5, 
                        boxstyle="round,pad=0.1", 
                        facecolor=colors['error'], 
                        edgecolor=colors['border'], 
                        linewidth=2)
    ax.add_patch(box)
    ax.text(3, y_pin_not_set, steps[5], fontsize=8, ha='center', va='center', wrap=True)
    
    # PIN Setup Process (Steps 7-10)
    pin_setup_steps = steps[6:10]
    for i, step in enumerate(pin_setup_steps):
        y = y_pin_not_set - (i + 1) * step_height
        box = FancyBboxPatch((7.5, y-0.25), 3, 0.5, 
                            boxstyle="round,pad=0.1", 
                            facecolor=colors['pin_setup'], 
                            edgecolor=colors['border'], 
                            linewidth=2)
        ax.add_patch(box)
        ax.text(9, y, step, fontsize=8, ha='center', va='center', wrap=True)
    
    # PIN Setup Complete (Step 11)
    y_pin_complete = y_pin_not_set - 5 * step_height
    box = FancyBboxPatch((4.5, y_pin_complete-0.25), 3, 0.5, 
                        boxstyle="round,pad=0.1", 
                        facecolor=colors['pin_setup'], 
                        edgecolor=colors['border'], 
                        linewidth=2)
    ax.add_patch(box)
    ax.text(6, y_pin_complete, steps[10], fontsize=8, ha='center', va='center', wrap=True)
    
    # PIN Validation (Step 12)
    y_pin_validation = y_pin_complete - step_height
    box = FancyBboxPatch((4.5, y_pin_validation-0.25), 3, 0.5, 
                        boxstyle="round,pad=0.1", 
                        facecolor=colors['registration'], 
                        edgecolor=colors['border'], 
                        linewidth=2)
    ax.add_patch(box)
    ax.text(6, y_pin_validation, steps[11], fontsize=8, ha='center', va='center', wrap=True)
    
    # User Authentication (Step 13)
    y_user_auth = y_pin_validation - step_height
    box = FancyBboxPatch((4.5, y_user_auth-0.25), 3, 0.5, 
                        boxstyle="round,pad=0.1", 
                        facecolor=colors['registration'], 
                        edgecolor=colors['border'], 
                        linewidth=2)
    ax.add_patch(box)
    ax.text(6, y_user_auth, steps[12], fontsize=8, ha='center', va='center', wrap=True)
    
    # Credential Creation (Step 14)
    y_cred_creation = y_user_auth - step_height
    box = FancyBboxPatch((4.5, y_cred_creation-0.25), 3, 0.5, 
                        boxstyle="round,pad=0.1", 
                        facecolor=colors['success'], 
                        edgecolor=colors['border'], 
                        linewidth=2)
    ax.add_patch(box)
    ax.text(6, y_cred_creation, steps[13], fontsize=8, ha='center', va='center', wrap=True)
    
    # Phase 3: Authentication (Steps 15-18)
    ax.text(9, y_start + 0.5, "Phase 3: Authentication" if language == 'en' else "第三阶段：身份验证", 
            fontsize=12, fontweight='bold', ha='center', va='center', color=colors['border'])
    
    # Authentication Request (Step 15)
    y_auth_start = y_start
    box = FancyBboxPatch((8.5, y_auth_start-0.25), 3, 0.5, 
                        boxstyle="round,pad=0.1", 
                        facecolor=colors['auth'], 
                        edgecolor=colors['border'], 
                        linewidth=2)
    ax.add_patch(box)
    ax.text(10, y_auth_start, steps[14], fontsize=8, ha='center', va='center', wrap=True)
    
    # Credential Lookup Decision
    y_lookup = y_auth_start - step_height
    ax.text(10, y_lookup, "Credential Lookup" if language == 'en' else "凭据查找", 
            fontsize=10, fontweight='bold', ha='center', va='center')
    
    # Credential Not Found (Step 16)
    y_not_found = y_lookup - step_height
    box = FancyBboxPatch((6.5, y_not_found-0.25), 3, 0.5, 
                        boxstyle="round,pad=0.1", 
                        facecolor=colors['error'], 
                        edgecolor=colors['border'], 
                        linewidth=2)
    ax.add_patch(box)
    ax.text(8, y_not_found, steps[15], fontsize=8, ha='center', va='center', wrap=True)
    
    # Credential Found - Success Path (Steps 17-18)
    success_steps = steps[16:18]
    for i, step in enumerate(success_steps):
        y = y_not_found - (i + 1) * step_height
        box = FancyBboxPatch((10.5, y-0.25), 3, 0.5, 
                            boxstyle="round,pad=0.1", 
                            facecolor=colors['success'], 
                            edgecolor=colors['border'], 
                            linewidth=2)
        ax.add_patch(box)
        ax.text(12, y, step, fontsize=8, ha='center', va='center', wrap=True)
    
    # Add arrows to show proper flow
    # From initialization to registration (Step 3 to Step 4)
    arrow1 = ConnectionPatch((3.5, y_start-1.5), (4.5, y_start), "data", "data",
                            arrowstyle="->", shrinkA=5, shrinkB=5, mutation_scale=20, fc=colors['border'])
    ax.add_patch(arrow1)
    
    # From registration to authentication (Step 14 to Step 15)
    arrow2 = ConnectionPatch((7.5, y_cred_creation), (8.5, y_auth_start), "data", "data",
                            arrowstyle="->", shrinkA=5, shrinkB=5, mutation_scale=20, fc=colors['border'])
    ax.add_patch(arrow2)
    
    # From Step 4 to Step 5 (MakeCredential to PIN check)
    arrow3 = ConnectionPatch((6, y_start-0.25), (6, y_start-step_height+0.25), "data", "data",
                            arrowstyle="->", shrinkA=5, shrinkB=5, mutation_scale=20, fc=colors['border'])
    ax.add_patch(arrow3)
    
    # From Step 5 to PIN decision
    arrow4 = ConnectionPatch((6, y_start-2*step_height-0.25), (6, y_pin+0.25), "data", "data",
                            arrowstyle="->", shrinkA=5, shrinkB=5, mutation_scale=20, fc=colors['border'])
    ax.add_patch(arrow4)
    
    # From PIN decision to PIN not set (Step 6)
    arrow5 = ConnectionPatch((4.5, y_pin), (3, y_pin_not_set), "data", "data",
                            arrowstyle="->", shrinkA=5, shrinkB=5, mutation_scale=20, fc=colors['border'])
    ax.add_patch(arrow5)
    
    # From PIN not set to PIN setup process (Step 6 to Step 7)
    arrow6 = ConnectionPatch((3, y_pin_not_set-0.25), (7.5, y_pin_not_set-step_height+0.25), "data", "data",
                            arrowstyle="->", shrinkA=5, shrinkB=5, mutation_scale=20, fc=colors['border'])
    ax.add_patch(arrow6)
    
    # From PIN setup process to PIN complete (Step 10 to Step 11)
    arrow7 = ConnectionPatch((9, y_pin_not_set-5*step_height+0.25), (6, y_pin_complete-0.25), "data", "data",
                            arrowstyle="->", shrinkA=5, shrinkB=5, mutation_scale=20, fc=colors['border'])
    ax.add_patch(arrow7)
    
    # From PIN complete to PIN validation (Step 11 to Step 12)
    arrow8 = ConnectionPatch((6, y_pin_complete-0.25), (6, y_pin_validation+0.25), "data", "data",
                            arrowstyle="->", shrinkA=5, shrinkB=5, mutation_scale=20, fc=colors['border'])
    ax.add_patch(arrow8)
    
    # From PIN validation to user auth (Step 12 to Step 13)
    arrow9 = ConnectionPatch((6, y_pin_validation-0.25), (6, y_user_auth+0.25), "data", "data",
                            arrowstyle="->", shrinkA=5, shrinkB=5, mutation_scale=20, fc=colors['border'])
    ax.add_patch(arrow9)
    
    # From user auth to credential creation (Step 13 to Step 14)
    arrow10 = ConnectionPatch((6, y_user_auth-0.25), (6, y_cred_creation+0.25), "data", "data",
                             arrowstyle="->", shrinkA=5, shrinkB=5, mutation_scale=20, fc=colors['border'])
    ax.add_patch(arrow10)
    
    # From credential lookup to credential not found (Step 15 to Step 16)
    arrow11 = ConnectionPatch((8.5, y_lookup), (8, y_not_found), "data", "data",
                             arrowstyle="->", shrinkA=5, shrinkB=5, mutation_scale=20, fc=colors['border'])
    ax.add_patch(arrow11)
    
    # From credential not found to success path (Step 16 to Step 17)
    arrow12 = ConnectionPatch((8, y_not_found-0.25), (10.5, y_not_found-step_height+0.25), "data", "data",
                             arrowstyle="->", shrinkA=5, shrinkB=5, mutation_scale=20, fc=colors['border'])
    ax.add_patch(arrow12)
    
    # From Step 17 to Step 18
    arrow13 = ConnectionPatch((12, y_not_found-step_height-0.25), (12, y_not_found-2*step_height+0.25), "data", "data",
                             arrowstyle="->", shrinkA=5, shrinkB=5, mutation_scale=20, fc=colors['border'])
    ax.add_patch(arrow13)
    
    # Add legend
    legend_elements = [
        patches.Patch(color=colors['init'], label='Initialization' if language == 'en' else '初始化'),
        patches.Patch(color=colors['registration'], label='Registration' if language == 'en' else '注册'),
        patches.Patch(color=colors['pin_setup'], label='PIN Setup' if language == 'en' else 'PIN设置'),
        patches.Patch(color=colors['auth'], label='Authentication' if language == 'en' else '认证'),
        patches.Patch(color=colors['success'], label='Success' if language == 'en' else '成功'),
        patches.Patch(color=colors['error'], label='Error' if language == 'en' else '错误')
    ]
    ax.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(0.98, 0.98))
    
    plt.tight_layout()
    return fig

def save_diagram(fig, filename, dpi=300):
    """Save the diagram as an image file"""
    fig.savefig(filename, dpi=dpi, bbox_inches='tight', facecolor='white')
    print(f"Diagram saved as {filename}")

def main():
    """Generate both English and Chinese diagrams"""
    
    # Create output directory if it doesn't exist
    os.makedirs('images', exist_ok=True)
    
    # Generate English diagram
    print("Generating English FIDO2 workflow diagram...")
    fig_en = create_fido2_workflow_diagram('en')
    save_diagram(fig_en, 'images/fido2_workflow_en.png')
    plt.close(fig_en)
    
    # Generate Chinese diagram
    print("Generating Chinese FIDO2 workflow diagram...")
    fig_zh = create_fido2_workflow_diagram('zh')
    save_diagram(fig_zh, 'images/fido2_workflow_zh.png')
    plt.close(fig_zh)
    
    print("All diagrams generated successfully!")

if __name__ == "__main__":
    main()
