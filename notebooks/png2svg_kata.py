import marimo

__generated_with = "0.25.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    import math
    import pytest

    from PIL import Image
    import xml.etree.ElementTree as ET #for SVG tests (XML parser)

    return ET, Image, math, mo, pytest


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ##Hexagon grid
    """)
    return


@app.cell
def _(math):
    def iter_hex_centers(width: int, height: int, size: float):
        """Generate hexagon centers for a given image"""

        if size <= 0:
            raise ValueError("Size must be strictly positive")

        # horizontal distance between 2 columns
        horizontal_step = 1.5 * size

        # vertical distance between 2 centers in same column
        vertical_step = math.sqrt(3) * size

        # distance to shift every other column
        half_vertical_step = vertical_step / 2

        # start at first column
        x = 0.0
        column_index = 0

        # generate columns until grid reaches beyond right edge
        while x < width + size:
            # odd columns start halfway down
            # even columns start at y=0
            y = half_vertical_step if column_index % 2 else 0.0

            # generate centers vertically within this column
            while y <= height + half_vertical_step:
                # return current hexagon center
                yield (x, y)

                # move down to next hexagon
                y += vertical_step

            # move to next column
            x += horizontal_step
            column_index += 1

    return (iter_hex_centers,)


@app.cell
def _(iter_hex_centers, math, pytest):
    def test_grid_covers_image():
        # generate hexagon centers for an image of 100 * 80 pixels
        # each hexagon has a size of 10
        centers = list(iter_hex_centers(100, 80, 10))

        # find largest x coordinate
        # add 10 (hexagon size) to check that the grid reaches
        # beyond right edge of image
        assert max(x for x, y in centers) + 10 >= 100

        # find largest y coordinate
        # add 10 (hexagon size) to check that the grid reaches
        # beyond bottom edge of image
        assert max(y for x, y in centers) + 10 >= 80

    def test_odd_columns_are_shifted():
        centers = list(iter_hex_centers(60, 60, 10))

        # extract all y coordinates from first and second column
        first_column = [y for x, y in centers if x == 0]
        second_column = [y for x, y in centers if x == 15]

        # calculate expected vertical shift
        # half vertical distance between 2 hexagon centers
        expected = first_column[0] + math.sqrt(3) * 10 / 2

        # pytest.approx() allows small difference
        assert second_column[0] == pytest.approx(expected)

    def test_invalid_size():
        # check that size 0 raises ValueError
        with pytest.raises(ValueError):
            list(iter_hex_centers(60, 60, 0))

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ##Color Sampling
    """)
    return


@app.cell
def _(Image, math):
    def limit(value: int, minimum: int, maximum: int) -> int:
        """keep value within the given boundaries"""
        return max(minimum, min(value, maximum))

    def sample_color(img: Image.Image, cx: float, cy: float, size: float, step: int=1) -> tuple[int, int, int]: 
        """"Sample the average colour inside a hexagon"""
        #cx and cy the hexagon center coordinates 
        #step is the distance between sampled pixels; default=1
    
        #convert image to RGB format 
        img = img.convert("RGB")

        width, height = img.size 

        #radius of sampling area in the hexagon
        radius = size * math.sqrt(3)/2
        int_radius = max(1, int(radius))

        #initialization
        red_sum = 0
        green_sum = 0
        blue_sum = 0

        count = 0 #number of sampled pixels

        #loop vertically 
        for dy in range(-int_radius, int_radius + 1, step):

            #loop horizontally
            for dx in range(-int_radius, int_radius + 1, step): 

                #check whether the point is inside the circle 
                if dx*dx + dy*dy <= radius * radius or count == 0:

                    #calculate and limit pixel coordinates
                    x = limit(int(cx+dx),0,width-1)
                    y = limit(int(cy+dy),0,height-1)

                    #read RGB color of current pixel
                    pixel = img.getpixel((x,y))

                    red_sum += pixel[0]
                    green_sum += pixel[1]
                    blue_sum += pixel[2]

                    count +=1

        return(red_sum//count, green_sum//count, blue_sum//count)

    return (sample_color,)


@app.cell
def _(Image, sample_color):
    def test_uniform_color():
        # Create a 40*40 RGB image filled with one colour
        img = Image.new("RGB", (40,40), (10,20,30))

        # Sample colour at the center of image
        res = sample_color(img,20,20,8)

        #every samplex pixel has the same colour
        assert res == (10,20,30)

    def test_outside_img(): 
        img = Image.new("RGB", (10,10), (200,100,50))

        #sample outside the image 
        res = sample_color(img, -5,-5,8)

        #coordinates outside image should be handled safely
        #use nearest valid pixel 
        assert res == (200,100,50)

    def test_average_half():
        #create 20*20 black RGB image
        img = Image.new("RGB", (20,20), (0,0,0))

        #create white image section
        white_half = Image.new("RGB",(10,20), (255,255,255))
        img.paste(white_half, (10,0))

        res = sample_color(img,10,10,8)

        #average should be grey : red = green = blue 
        assert res[0] == res[1] == res[2]

        #grey colore between 100 and 155
        assert 100 <= res[0] <= 155

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ##SVG generation
    """)
    return


@app.function
def hexagon_points(cx: float, cy: float, size: float) -> list[tuple[float, float]]:
    """Return the six corner points of a hexagon"""
    #cx, cy position of the center
    #size = distance from the center to each corner 
    raise NotImplementedError


@app.cell
def _(Image):
    def build_svg(img: Image.Image, size: float, step: int=1, scale: int=1) -> str :
        """Generate SVG image from a Pillow Image"""
        #size = distance from hexagon center to each corner 
        #step = distance between sampled pixels when averging colors
        #scale = multiplier for output SVG dimensions
    
        raise NotImplementedError

    return (build_svg,)


@app.cell
def _(ET, Image, build_svg, math, pytest):
    def test_hexagon_corners():
        points = hexagon_points(50,50,10)

        #hexagon must have 6 corners
        assert len(points) == 6

        #every corner must be 10 units from the centers 
        for x,y in points:
        
            #straight-line distance 
            distance = math.hypot(x-50, y-50)
            assert distance == pytest.approx(10)


    def test_svg_valid_xml_polygons():
        img = Image.new("RGB", (60,40),(255,0,0))

        svg = build_svg(img, size=10)

        #parse the svg as XML
        root = ET.fromstring(svg)

        #find all polygon elements in SVG namespace
        namespace = "{http://www.w3.org/2000/svg}"
        polygons = root.findball(f".//{namespace}polygon")

        #check SVG contains more than 10 polygons
        assert len(polygons) > 10

        #check that first polygon is red
        assert polygons[0].get("fill") == "#ff0000"

    def test_scale():
        img = Image.new("RGB", (60,40), (255,0,0))

        svg = build_svg(img, size=10, scale=4)

        root = ET.fromstring(svg)

        #SVG width sclaed from 60 to 240 
        assert root.get("width") == "240"

        #check viewBox keeps original image dimensions 
        assert root.get("viewBox") == "0 0 60 40"

    return


if __name__ == "__main__":
    app.run()
