import marimo

__generated_with = "0.25.2"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _():
    import io

    import marimo as mo
    from PIL import Image

    from png2svg import build_svg

    return Image, build_svg, io, mo


@app.cell(hide_code=True)
def _(mo):
    # widget for uploading an image
    upload = mo.ui.file(filetypes=[".png", ".jpg", ".jpeg"], label="Upload and image")

    # Slider to choose hexagon size
    size_slider = mo.ui.slider(start=3, stop=60, value=10, label="Hexagon size")

    # Dropdown to choose hexagon orientation
    orientation_dropdown = mo.ui.dropdown(
        options=["flat", "pointy"], value="flat", label="Orientation"
    )

    # Display all three controls
    mo.vstack([upload, size_slider, orientation_dropdown])
    return orientation_dropdown, size_slider, upload


@app.cell(hide_code=True)
def _(Image, build_svg, io, mo, orientation_dropdown, size_slider, upload):
    svg = None

    # stop here if no image has been uploaded
    if not upload.value:
        preview = mo.md("Please upload a PNG or JPG image to get started")

    else:
        # Read uploaded image
        img_bytes = upload.value[0].contents
        img = Image.open(io.BytesIO(img_bytes))

        svg = build_svg(
            img, size=size_slider.value, orientation=orientation_dropdown.value
        )

        # Remove XML declaration because mo.Html expects SVG markup
        svg_content = svg.split("\n", 1)[1] if svg.startswith("<?xml") else svg

        # Display the generated SVG
        preview = mo.Html(svg_content)

    mo.vstack([preview])
    return (svg,)


@app.cell(hide_code=True)
def _(mo, svg):
    # Only display the download button when an image is uploaded
    if svg is not None:
        download_button = mo.download(
            data=svg.encode("utf-8"),
            filename="converted_image.svg",
            mimetype="image/svg+xml",
            label="Download SVG",
        )

    else:
        download_button = mo.md("Upload an image to enable SVG download")

    mo.vstack([download_button])


if __name__ == "__main__":
    app.run()
