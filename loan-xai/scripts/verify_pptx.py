import zipfile
from pptx import Presentation

pptx_path = r'C:\bava\loan-xai\loan-xai-presentation.pptx'
with zipfile.ZipFile(pptx_path, 'r') as z:
    file_list = z.namelist()
    print(f"Zip valid. Total files in OpenXML archive: {len(file_list)}")

prs = Presentation(pptx_path)
print(f"Slide count: {len(prs.slides)}")
print(f"Dimensions: {prs.slide_width.inches:.3f}\" x {prs.slide_height.inches:.3f}\"")

for idx, slide in enumerate(prs.slides):
    notes = slide.notes_slide.notes_text_frame.text if slide.has_notes_slide else ""
    word_count = len(notes.split())
    has_image = any(shape.shape_type == 13 for shape in slide.shapes)  # 13 is picture
    print(f"Slide {idx+1:2d}: {len(slide.shapes):2d} shapes | Has image: {str(has_image):5s} | Notes words: {word_count}")

print("Verification completed successfully!")
