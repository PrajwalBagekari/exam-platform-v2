import os
import shutil
import gc


def cleanup_processing_files(
    pdf_path=None,
    rendered_pages_dir=None,
):
    try:
        if pdf_path and os.path.exists(pdf_path):
            os.remove(pdf_path)
            print(f"Deleted PDF: {pdf_path}")
    except Exception as e:
        print(f"PDF cleanup failed: {e}")

    try:
        if rendered_pages_dir and os.path.exists(rendered_pages_dir):
            shutil.rmtree(rendered_pages_dir)

            # recreate empty folder
            os.makedirs(
                rendered_pages_dir,
                exist_ok=True
            )

            print("Rendered pages cleaned")

    except Exception as e:
        print(f"Rendered pages cleanup failed: {e}")

    gc.collect()

    print("Cleanup completed")