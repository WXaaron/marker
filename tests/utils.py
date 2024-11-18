from marker.v2.providers.pdf import PdfProvider
import tempfile

import datasets
from marker.v2.models import setup_layout_model, setup_recognition_model, setup_detection_model
from marker.v2.builders.document import DocumentBuilder
from marker.v2.builders.layout import LayoutBuilder
from marker.v2.builders.ocr import OcrBuilder
from marker.v2.schema.document import Document


def setup_pdf_document(
    filename='adversarial.pdf',
    config=None,
) -> Document:
    dataset = datasets.load_dataset("datalab-to/pdfs", split="train")
    idx = dataset['filename'].index(filename)

    temp_pdf = tempfile.NamedTemporaryFile(suffix=".pdf")
    temp_pdf.write(dataset['pdf'][idx])
    temp_pdf.flush()

    layout_model = setup_layout_model()
    recognition_model = setup_recognition_model()
    detection_model = setup_detection_model()

    provider = PdfProvider(temp_pdf.name, config)
    layout_builder = LayoutBuilder(layout_model, config)
    ocr_builder = OcrBuilder(detection_model, recognition_model, config)
    builder = DocumentBuilder(config)
    document = builder(provider, layout_builder, ocr_builder)
    return document
