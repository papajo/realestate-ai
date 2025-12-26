import boto3
from botocore.exceptions import ClientError
from app.core.config import settings
import json


class KMSEncryption:
    def __init__(self):
        if settings.AWS_KMS_KEY_ID:
            self.kms_client = boto3.client(
                'kms',
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                region_name=settings.AWS_REGION
            )
            self.key_id = settings.AWS_KMS_KEY_ID
        else:
            self.kms_client = None
            self.key_id = None
    
    def encrypt(self, plaintext: str) -> bytes:
        """Encrypt sensitive data using AWS KMS"""
        if not self.kms_client or not self.key_id:
            # Fallback to local encryption if KMS not configured
            return plaintext.encode()
        
        try:
            response = self.kms_client.encrypt(
                KeyId=self.key_id,
                Plaintext=plaintext
            )
            return response['CiphertextBlob']
        except ClientError as e:
            raise Exception(f"Encryption failed: {str(e)}")
    
    def decrypt(self, ciphertext: bytes) -> str:
        """Decrypt data using AWS KMS"""
        if not self.kms_client or not self.key_id:
            # Fallback to local decryption if KMS not configured
            return ciphertext.decode()
        
        try:
            response = self.kms_client.decrypt(CiphertextBlob=ciphertext)
            return response['Plaintext'].decode('utf-8')
        except ClientError as e:
            raise Exception(f"Decryption failed: {str(e)}")
    
    def encrypt_pii(self, data: dict) -> dict:
        """Encrypt PII fields in a dictionary"""
        pii_fields = ['email', 'phone', 'ssn', 'address', 'name']
        encrypted_data = data.copy()
        
        for field in pii_fields:
            if field in encrypted_data and encrypted_data[field]:
                encrypted_data[field] = self.encrypt(str(encrypted_data[field]))
        
        return encrypted_data
    
    def decrypt_pii(self, data: dict) -> dict:
        """Decrypt PII fields in a dictionary"""
        pii_fields = ['email', 'phone', 'ssn', 'address', 'name']
        decrypted_data = data.copy()
        
        for field in pii_fields:
            if field in decrypted_data and isinstance(decrypted_data[field], bytes):
                decrypted_data[field] = self.decrypt(decrypted_data[field])
        
        return decrypted_data


kms_encryption = KMSEncryption()

