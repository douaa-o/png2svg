import marimo

__generated_with = "0.25.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import math
    import pytest 
    from PIL import Image

    return math, pytest


@app.cell
def _(math):
    def iter_hex_centers(width: int, height: int, size: float) :
        """generate hexagon centers for a given image""" 

        if size <= 0 : 
            raise ValueError("Size must be strictly positive")

        #horizontal distance between 2 columns
        horizontal_step = 1.5 * size 
    
        #vertical distance between 2 centers
        vertical_step = math.sqrt(3) * size 

        #distance to shift every other column
        half_vertical_step = vertical_step/2

        x = 0.0
        column_index = 0

        #generate columns until grid reaches beyond right edge 
        while x < width + size :
        
            #odd columns start halfway 
            #even columns start at y=0
            if column_index % 2 :
                y = half_vertical_step 
            else: 
                y = 0.0

            #generate centers vertically within this column
            while y <= height + half_vertical_step:

                #return current hexagon center
                yield(x,y)

                #move down to next hexagon
                y += vertical_step
            
            #move to next column
            x += horizontal_step
            column_index +=1
        

    return (iter_hex_centers,)


@app.cell
def _(iter_hex_centers, math, pytest):
    def test_grid_covers_image(): 
        #generate hexagon centers for an image of 100 * 80 pixels
        #each hexagon has a size of 10
        centers = list(iter_hex_centers(100, 80, 10))

        #find largest x coordinate
        #add 10 (hexagon size) to check that the grid reaches
        #beyond right edge of image
        assert max(x for x, y in centers) + 10 >= 100

        #find largest y coordinate
        #add 10 (hexagon size) to check that the grid reaches
        #beyond bottom edge of image
        assert max(y for x, y in centers) + 10 >= 80

    def test_odd_columns_are_shifted():
        centers = list(iter_hex_centers(60, 60, 10))

        #extract all y coordinates from first and second column
        first_column = [y for x,y in centers if x == 0]
        second_column = [y for x,y in centers if x == 15]

        #calculate expected vertical shift
        #half vertical distance between 2 hexagon centers
        expected = first_column[0] + math.sqrt(3) * 10/2

        #pytest.approx() allows small difference
        assert second_column[0] == pytest.approx(expected)

    def test_invalid_size():
        #check that size 0 raises ValueError
        with pytest.raises(ValueError):
            list(iter_hex_centers(60, 60, 0))

    return


if __name__ == "__main__":
    app.run()
