"""
Script upload model PhoBERT fine-tuned lên HuggingFace Hub.

Hướng dẫn:
1. Tạo tài khoản tại https://huggingface.co
2. Tạo Access Token tại https://huggingface.co/settings/tokens (chọn "Write")
3. Chạy script:
   python upload_model.py

Script sẽ hỏi bạn:
- HuggingFace username
- Tên repo (mặc định: phobert-sentiment-vietnamese)
- Access Token
"""

import os

def main():
    try:
        from huggingface_hub import HfApi, login
    except ImportError:
        print("❌ Cần cài huggingface_hub. Chạy:")
        print("   pip install huggingface_hub")
        return

    print("=" * 50)
    print("📤 Upload PhoBERT Model lên HuggingFace Hub")
    print("=" * 50)

    # Nhập thông tin
    username = input("\n👤 HuggingFace username: ").strip()
    repo_name = input("📁 Tên repo (Enter = phobert-sentiment-vietnamese): ").strip()
    if not repo_name:
        repo_name = "phobert-sentiment-vietnamese"
    token = input("🔑 Access Token (Write): ").strip()

    repo_id = f"{username}/{repo_name}"
    model_dir = os.path.join(os.path.dirname(__file__), "models", "phobert_best")

    if not os.path.exists(model_dir):
        print(f"❌ Không tìm thấy thư mục: {model_dir}")
        return

    print(f"\n📦 Đang upload {model_dir} → {repo_id}...")

    try:
        login(token=token)
        api = HfApi()

        # Tạo repo nếu chưa có
        api.create_repo(repo_id=repo_id, exist_ok=True)

        # Upload toàn bộ thư mục model
        api.upload_folder(
            folder_path=model_dir,
            repo_id=repo_id,
            commit_message="Upload PhoBERT sentiment model fine-tuned"
        )

        print(f"\n✅ Upload thành công!")
        print(f"🔗 Link: https://huggingface.co/{repo_id}")
        print(f"\n💡 Hãy cập nhật HUGGINGFACE_REPO_ID trong core/models.py:")
        print(f'   HUGGINGFACE_REPO_ID = "{repo_id}"')

    except Exception as e:
        print(f"\n❌ Lỗi: {e}")


if __name__ == "__main__":
    main()
