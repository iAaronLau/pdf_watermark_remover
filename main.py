from itertools import product
import fitz
import multiprocessing
from pathlib import Path

WATERMARK_RGB = (137, 170, 209)  # The RGB value of the watermark you want to remove


def remove_func(src_pdf_path, book_name, page_num):
    print(page_num, src_pdf_path)
    mat = fitz.Matrix(3, 3)
    pdf = fitz.open(src_pdf_path)
    page = pdf[page_num]

    pixmap = page.get_pixmap(matrix=mat, alpha=False)
    for pos in product(range(pixmap.width), range(pixmap.height)):
        rgb = pixmap.pixel(pos[0], pos[1])
        if (sum(rgb) >= sum(WATERMARK_RGB)):
            pixmap.set_pixel(pos[0], pos[1], (255, 255, 255))
    pixmap.pil_save("pdf_images/{}/{}.jpg".format(book_name, page_num))


class Remove_pdf():
    def __init__(self, src_pdf_path="example.pdf"):
        self.src_pdf_path = src_pdf_path
        self.pdf = fitz.open(src_pdf_path)
        self.book_name = src_pdf_path.lower().replace(".pdf", "").replace(" ", "")
        self.thread_pool = multiprocessing.Pool(processes=8)
        Path("pdf_images/{}".format(self.book_name)).mkdir(parents=True, exist_ok=True)

    def remove(self):
        for page_num, _ in enumerate(self.pdf):
            self.thread_pool.apply_async(remove_func, args=(
                self.src_pdf_path,
                self.book_name,
                page_num,
            ))
        self.thread_pool.close()
        self.thread_pool.join()


if __name__ == '__main__':
    a = Remove_pdf("example.pdf")
    a.remove()
