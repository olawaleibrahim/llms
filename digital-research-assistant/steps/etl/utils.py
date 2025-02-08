from digital_research_assistant.application.extractors import PDFExtractor, WordExtractor


def use_extractor(filepath):

    extension = filepath.split(".")[-1]
    extractors_dict = {"docx": WordExtractor(),
                       "doc": WordExtractor(), "pdf": PDFExtractor()}

    return extractors_dict[extension]
