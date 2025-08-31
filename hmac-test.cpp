QByteArray Fido::computeHMACSHA256(const QByteArray& key, const QByteArray& data) const
{
	try {
		printf("DEBUG: computeHMACSHA256 - key size: %d, data size: %d\n", key.size(), data.size());
		
		// 使用 OpenSSL 实现 HMAC-SHA-256
		unsigned char hmac[EVP_MAX_MD_SIZE];
		unsigned int hmacLen = 0;
		
		// 创建 HMAC 上下文
		HMAC_CTX* hmacCtx = HMAC_CTX_new();
		if (!hmacCtx) {
			printf("ERROR: Failed to create HMAC context\n");
			return QByteArray();
		}
		
		// 初始化 HMAC 计算
		if (HMAC_Init_ex(hmacCtx, key.data(), key.size(), EVP_sha256(), nullptr) != 1) {
			printf("ERROR: Failed to initialize HMAC\n");
			HMAC_CTX_free(hmacCtx);
			return QByteArray();
		}
		
		// 更新数据
		if (HMAC_Update(hmacCtx, reinterpret_cast<const unsigned char*>(data.data()), data.size()) != 1) {
			printf("ERROR: Failed to update HMAC\n");
			HMAC_CTX_free(hmacCtx);
			return QByteArray();
		}
		
		// 完成 HMAC 计算
		if (HMAC_Final(hmacCtx, hmac, &hmacLen) != 1) {
			printf("ERROR: Failed to finalize HMAC\n");
			HMAC_CTX_free(hmacCtx);
			return QByteArray();
		}
		
		// 清理上下文
		HMAC_CTX_free(hmacCtx);
		
		// 返回计算出的 HMAC 值
		QByteArray result(reinterpret_cast<const char*>(hmac), hmacLen);
		printf("DEBUG: HMAC-SHA-256 computed successfully, length: %d\n", result.size());
		
		return result;
		
	} catch (const std::exception& e) {
		printf("ERROR: HMAC-SHA-256 computation failed: %s\n", e.what());
		return QByteArray();
	}
}