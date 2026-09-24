class Border:
    LIGHT = "light"
    HEAVY = "heavy"
    DOUBLE = "double"
    ROUND = "round"
    
    # Light
    TOP_LEFT_CORNER_LIGHT = '┌'
    TOP_RIGHT_CORNER_LIGHT = '┐'
    BOTTOM_LEFT_CORNER_LIGHT = '└'
    BOTTOM_RIGHT_CORNER_LIGHT = '┘'
    TOP_T_LIGHT = '┬'
    BOTTOM_T_LIGHT = '┴'
    LEFT_T_LIGHT = '├'
    RIGHT_T_LIGHT = '┤'
    CROSS_LIGHT = '┼'
    HORIZONTAL_LIGHT = '─'
    VERTICAL_LIGHT = '│'

    # Heavy
    TOP_LEFT_CORNER_HEAVY = '┏'
    TOP_RIGHT_CORNER_HEAVY = '┓'
    BOTTOM_LEFT_CORNER_HEAVY = '┗'
    BOTTOM_RIGHT_CORNER_HEAVY = '┛'
    TOP_T_HEAVY = '┳'
    BOTTOM_T_HEAVY = '┻'
    LEFT_T_HEAVY = '┣'
    RIGHT_T_HEAVY = '┫'
    CROSS_HEAVY = '╋'
    HORIZONTAL_HEAVY = '━'
    VERTICAL_HEAVY = '┃'

    # Double
    TOP_LEFT_CORNER_DOUBLE = '╔'
    TOP_RIGHT_CORNER_DOUBLE = '╗'
    BOTTOM_LEFT_CORNER_DOUBLE = '╚'
    BOTTOM_RIGHT_CORNER_DOUBLE = '╝'
    TOP_T_DOUBLE = '╦'
    BOTTOM_T_DOUBLE = '╩'
    LEFT_T_DOUBLE = '╠'
    RIGHT_T_DOUBLE = '╣'
    CROSS_DOUBLE = '╬'
    HORIZONTAL_DOUBLE = '═'
    VERTICAL_DOUBLE = '║'

    # Rounded Corners
    TOP_LEFT_CORNER_ROUNDED = '╭'
    TOP_RIGHT_CORNER_ROUNDED = '╮'
    BOTTOM_LEFT_CORNER_ROUNDED = '╰'
    BOTTOM_RIGHT_CORNER_ROUNDED = '╯'
    TOP_T_ROUNDED = '┬'
    BOTTOM_T_ROUNDED = '┴'
    LEFT_T_ROUNDED = '├'
    RIGHT_T_ROUNDED = '┤'
    CROSS_ROUNDED = '┼'
    HORIZONTAL_ROUNDED = '─'
    VERTICAL_ROUNDED = '│'

    @staticmethod
    def get_border_chars(type):
        if type == Border.LIGHT:
            return {
                "top_left_corner": Border.TOP_LEFT_CORNER_LIGHT,
                "top_right_corner": Border.TOP_RIGHT_CORNER_LIGHT,
                "bottom_left_corner": Border.BOTTOM_LEFT_CORNER_LIGHT,
                "bottom_right_corner": Border.BOTTOM_RIGHT_CORNER_LIGHT,
                "top_t": Border.TOP_T_LIGHT,
                "bottom_t": Border.BOTTOM_T_LIGHT,
                "left_t": Border.LEFT_T_LIGHT,
                "right_t": Border.RIGHT_T_LIGHT,
                "cross": Border.CROSS_LIGHT,
                "horizontal": Border.HORIZONTAL_LIGHT,
                "vertical": Border.VERTICAL_LIGHT
            }
        elif type == Border.HEAVY:
            return {
                "top_left_corner": Border.TOP_LEFT_CORNER_HEAVY,
                "top_right_corner": Border.TOP_RIGHT_CORNER_HEAVY,
                "bottom_left_corner": Border.BOTTOM_LEFT_CORNER_HEAVY,
                "bottom_right_corner": Border.BOTTOM_RIGHT_CORNER_HEAVY,
                "top_t": Border.TOP_T_HEAVY,
                "bottom_t": Border.BOTTOM_T_HEAVY,
                "left_t": Border.LEFT_T_HEAVY,
                "right_t": Border.RIGHT_T_HEAVY,
                "cross": Border.CROSS_HEAVY,
                "horizontal": Border.HORIZONTAL_HEAVY,
                "vertical": Border.VERTICAL_HEAVY
            }
        elif type == Border.DOUBLE:
            return {
                "top_left_corner": Border.TOP_LEFT_CORNER_DOUBLE,
                "top_right_corner": Border.TOP_RIGHT_CORNER_DOUBLE,
                "bottom_left_corner": Border.BOTTOM_LEFT_CORNER_DOUBLE,
                "bottom_right_corner": Border.BOTTOM_RIGHT_CORNER_DOUBLE,
                "top_t": Border.TOP_T_DOUBLE,
                "bottom_t": Border.BOTTOM_T_DOUBLE,
                "left_t": Border.LEFT_T_DOUBLE,
                "right_t": Border.RIGHT_T_DOUBLE,
                "cross": Border.CROSS_DOUBLE,
                "horizontal": Border.HORIZONTAL_DOUBLE,
                "vertical": Border.VERTICAL_DOUBLE
            }
        elif type == Border.ROUND:
            return {
                "top_left_corner": Border.TOP_LEFT_CORNER_ROUNDED,
                "top_right_corner": Border.TOP_RIGHT_CORNER_ROUNDED,
                "bottom_left_corner": Border.BOTTOM_LEFT_CORNER_ROUNDED,
                "bottom_right_corner": Border.BOTTOM_RIGHT_CORNER_ROUNDED,
                "top_t": Border.TOP_T_ROUNDED,
                "bottom_t": Border.BOTTOM_T_ROUNDED,
                "left_t": Border.LEFT_T_ROUNDED,
                "right_t": Border.RIGHT_T_ROUNDED,
                "cross": Border.CROSS_ROUNDED,
                "horizontal": Border.HORIZONTAL_ROUNDED,
                "vertical": Border.VERTICAL_ROUNDED
            }
        return {}