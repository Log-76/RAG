"""
Utility module for formatting and displaying terminal output with ANSI colors.
"""

from typing import NamedTuple


# ----------------------------------------------------------------------------
#  Formatter
# ----------------------------------------------------------------------------

class ColorFormat(NamedTuple):
    """
    Defines a mapping between a color name and its corresponding ANSI escape
    code.
    """
    name: str
    ansi: str


class TerminalFormatter:
    """
    Provides methods to apply ANSI color codes and styles to terminal text.
    """
    # ANSI Reset
    RESET: ColorFormat = ColorFormat("reset", "\033[0m")

    # ANSI Foreground Colors (30-37)
    BLACK: ColorFormat = ColorFormat("black", "\033[30m")
    DARK_RED: ColorFormat = ColorFormat("dark_red", "\033[31m")
    DARK_GREEN: ColorFormat = ColorFormat("dark_green", "\033[32m")
    DARK_YELLOW: ColorFormat = ColorFormat("dark_yellow", "\033[33m")
    DARK_BLUE: ColorFormat = ColorFormat("dark_blue", "\033[34m")
    DARK_MAGENTA: ColorFormat = ColorFormat("dark_magenta", "\033[35m")
    DARK_CYAN: ColorFormat = ColorFormat("dark_cyan", "\033[36m")
    LIGHT_GRAY: ColorFormat = ColorFormat("light_gray", "\033[37m")

    # ANSI Background Colors (40-47)
    BG_BLACK: ColorFormat = ColorFormat("bg_black", "\033[40m")
    BG_RED: ColorFormat = ColorFormat("bg_red", "\033[41m")
    BG_GREEN: ColorFormat = ColorFormat("bg_green", "\033[42m")
    BG_YELLOW: ColorFormat = ColorFormat("bg_yellow", "\033[43m")
    BG_BLUE: ColorFormat = ColorFormat("bg_blue", "\033[44m")
    BG_MAGENTA: ColorFormat = ColorFormat("bg_magenta", "\033[45m")
    BG_CYAN: ColorFormat = ColorFormat("bg_cyan", "\033[46m")
    BG_WHITE: ColorFormat = ColorFormat("bg_white", "\033[47m")

    # High Intensity Foreground Colors (90-97)
    GRAY: ColorFormat = ColorFormat("gray", "\033[90m")
    RED: ColorFormat = ColorFormat("red", "\033[91m")
    GREEN: ColorFormat = ColorFormat("green", "\033[92m")
    YELLOW: ColorFormat = ColorFormat("yellow", "\033[93m")
    BLUE: ColorFormat = ColorFormat("blue", "\033[94m")
    MAGENTA: ColorFormat = ColorFormat("magenta", "\033[95m")
    CYAN: ColorFormat = ColorFormat("cyan", "\033[96m")
    WHITE: ColorFormat = ColorFormat("white", "\033[97m")

    # 256-Color Palette (016-231)
    COLOR_016: ColorFormat = ColorFormat("016", "\033[38;5;16m")
    COLOR_017: ColorFormat = ColorFormat("017", "\033[38;5;17m")
    COLOR_018: ColorFormat = ColorFormat("018", "\033[38;5;18m")
    COLOR_019: ColorFormat = ColorFormat("019", "\033[38;5;19m")
    COLOR_020: ColorFormat = ColorFormat("020", "\033[38;5;20m")
    COLOR_021: ColorFormat = ColorFormat("021", "\033[38;5;21m")
    COLOR_022: ColorFormat = ColorFormat("022", "\033[38;5;22m")
    COLOR_023: ColorFormat = ColorFormat("023", "\033[38;5;23m")
    COLOR_024: ColorFormat = ColorFormat("024", "\033[38;5;24m")
    COLOR_025: ColorFormat = ColorFormat("025", "\033[38;5;25m")
    COLOR_026: ColorFormat = ColorFormat("026", "\033[38;5;26m")
    COLOR_027: ColorFormat = ColorFormat("027", "\033[38;5;27m")
    COLOR_028: ColorFormat = ColorFormat("028", "\033[38;5;28m")
    COLOR_029: ColorFormat = ColorFormat("029", "\033[38;5;29m")
    COLOR_030: ColorFormat = ColorFormat("030", "\033[38;5;30m")
    COLOR_031: ColorFormat = ColorFormat("031", "\033[38;5;31m")
    COLOR_032: ColorFormat = ColorFormat("032", "\033[38;5;32m")
    COLOR_033: ColorFormat = ColorFormat("033", "\033[38;5;33m")
    COLOR_034: ColorFormat = ColorFormat("034", "\033[38;5;34m")
    COLOR_035: ColorFormat = ColorFormat("035", "\033[38;5;35m")
    COLOR_036: ColorFormat = ColorFormat("036", "\033[38;5;36m")
    COLOR_037: ColorFormat = ColorFormat("037", "\033[38;5;37m")
    COLOR_038: ColorFormat = ColorFormat("038", "\033[38;5;38m")
    COLOR_039: ColorFormat = ColorFormat("039", "\033[38;5;39m")
    COLOR_040: ColorFormat = ColorFormat("040", "\033[38;5;40m")
    COLOR_041: ColorFormat = ColorFormat("041", "\033[38;5;41m")
    COLOR_042: ColorFormat = ColorFormat("042", "\033[38;5;42m")
    COLOR_043: ColorFormat = ColorFormat("043", "\033[38;5;43m")
    COLOR_044: ColorFormat = ColorFormat("044", "\033[38;5;44m")
    COLOR_045: ColorFormat = ColorFormat("045", "\033[38;5;45m")
    COLOR_046: ColorFormat = ColorFormat("046", "\033[38;5;46m")
    COLOR_047: ColorFormat = ColorFormat("047", "\033[38;5;47m")
    COLOR_048: ColorFormat = ColorFormat("048", "\033[38;5;48m")
    COLOR_049: ColorFormat = ColorFormat("049", "\033[38;5;49m")
    COLOR_050: ColorFormat = ColorFormat("050", "\033[38;5;50m")
    COLOR_051: ColorFormat = ColorFormat("051", "\033[38;5;51m")
    COLOR_052: ColorFormat = ColorFormat("052", "\033[38;5;52m")
    COLOR_053: ColorFormat = ColorFormat("053", "\033[38;5;53m")
    COLOR_054: ColorFormat = ColorFormat("054", "\033[38;5;54m")
    COLOR_055: ColorFormat = ColorFormat("055", "\033[38;5;55m")
    COLOR_056: ColorFormat = ColorFormat("056", "\033[38;5;56m")
    COLOR_057: ColorFormat = ColorFormat("057", "\033[38;5;57m")
    COLOR_058: ColorFormat = ColorFormat("058", "\033[38;5;58m")
    COLOR_059: ColorFormat = ColorFormat("059", "\033[38;5;59m")
    COLOR_060: ColorFormat = ColorFormat("060", "\033[38;5;60m")
    COLOR_061: ColorFormat = ColorFormat("061", "\033[38;5;61m")
    COLOR_062: ColorFormat = ColorFormat("062", "\033[38;5;62m")
    COLOR_063: ColorFormat = ColorFormat("063", "\033[38;5;63m")
    COLOR_064: ColorFormat = ColorFormat("064", "\033[38;5;64m")
    COLOR_065: ColorFormat = ColorFormat("065", "\033[38;5;65m")
    COLOR_066: ColorFormat = ColorFormat("066", "\033[38;5;66m")
    COLOR_067: ColorFormat = ColorFormat("067", "\033[38;5;67m")
    COLOR_068: ColorFormat = ColorFormat("068", "\033[38;5;68m")
    COLOR_069: ColorFormat = ColorFormat("069", "\033[38;5;69m")
    COLOR_070: ColorFormat = ColorFormat("070", "\033[38;5;70m")
    COLOR_071: ColorFormat = ColorFormat("071", "\033[38;5;71m")
    COLOR_072: ColorFormat = ColorFormat("072", "\033[38;5;72m")
    COLOR_073: ColorFormat = ColorFormat("073", "\033[38;5;73m")
    COLOR_074: ColorFormat = ColorFormat("074", "\033[38;5;74m")
    COLOR_075: ColorFormat = ColorFormat("075", "\033[38;5;75m")
    COLOR_076: ColorFormat = ColorFormat("076", "\033[38;5;76m")
    COLOR_077: ColorFormat = ColorFormat("077", "\033[38;5;77m")
    COLOR_078: ColorFormat = ColorFormat("078", "\033[38;5;78m")
    COLOR_079: ColorFormat = ColorFormat("079", "\033[38;5;79m")
    COLOR_080: ColorFormat = ColorFormat("080", "\033[38;5;80m")
    COLOR_081: ColorFormat = ColorFormat("081", "\033[38;5;81m")
    COLOR_082: ColorFormat = ColorFormat("082", "\033[38;5;82m")
    COLOR_083: ColorFormat = ColorFormat("083", "\033[38;5;83m")
    COLOR_084: ColorFormat = ColorFormat("084", "\033[38;5;84m")
    COLOR_085: ColorFormat = ColorFormat("085", "\033[38;5;85m")
    COLOR_086: ColorFormat = ColorFormat("086", "\033[38;5;86m")
    COLOR_087: ColorFormat = ColorFormat("087", "\033[38;5;87m")
    COLOR_088: ColorFormat = ColorFormat("088", "\033[38;5;88m")
    COLOR_089: ColorFormat = ColorFormat("089", "\033[38;5;89m")
    COLOR_090: ColorFormat = ColorFormat("090", "\033[38;5;90m")
    COLOR_091: ColorFormat = ColorFormat("091", "\033[38;5;91m")
    COLOR_092: ColorFormat = ColorFormat("092", "\033[38;5;92m")
    COLOR_093: ColorFormat = ColorFormat("093", "\033[38;5;93m")
    COLOR_094: ColorFormat = ColorFormat("094", "\033[38;5;94m")
    COLOR_095: ColorFormat = ColorFormat("095", "\033[38;5;95m")
    COLOR_096: ColorFormat = ColorFormat("096", "\033[38;5;96m")
    COLOR_097: ColorFormat = ColorFormat("097", "\033[38;5;97m")
    COLOR_098: ColorFormat = ColorFormat("098", "\033[38;5;98m")
    COLOR_099: ColorFormat = ColorFormat("099", "\033[38;5;99m")
    COLOR_100: ColorFormat = ColorFormat("100", "\033[38;5;100m")
    COLOR_101: ColorFormat = ColorFormat("101", "\033[38;5;101m")
    COLOR_102: ColorFormat = ColorFormat("102", "\033[38;5;102m")
    COLOR_103: ColorFormat = ColorFormat("103", "\033[38;5;103m")
    COLOR_104: ColorFormat = ColorFormat("104", "\033[38;5;104m")
    COLOR_105: ColorFormat = ColorFormat("105", "\033[38;5;105m")
    COLOR_106: ColorFormat = ColorFormat("106", "\033[38;5;106m")
    COLOR_107: ColorFormat = ColorFormat("107", "\033[38;5;107m")
    COLOR_108: ColorFormat = ColorFormat("108", "\033[38;5;108m")
    COLOR_109: ColorFormat = ColorFormat("109", "\033[38;5;109m")
    COLOR_110: ColorFormat = ColorFormat("110", "\033[38;5;110m")
    COLOR_111: ColorFormat = ColorFormat("111", "\033[38;5;111m")
    COLOR_112: ColorFormat = ColorFormat("112", "\033[38;5;112m")
    COLOR_113: ColorFormat = ColorFormat("113", "\033[38;5;113m")
    COLOR_114: ColorFormat = ColorFormat("114", "\033[38;5;114m")
    COLOR_115: ColorFormat = ColorFormat("115", "\033[38;5;115m")
    COLOR_116: ColorFormat = ColorFormat("116", "\033[38;5;116m")
    COLOR_117: ColorFormat = ColorFormat("117", "\033[38;5;117m")
    COLOR_118: ColorFormat = ColorFormat("118", "\033[38;5;118m")
    COLOR_119: ColorFormat = ColorFormat("119", "\033[38;5;119m")
    COLOR_120: ColorFormat = ColorFormat("120", "\033[38;5;120m")
    COLOR_121: ColorFormat = ColorFormat("121", "\033[38;5;121m")
    COLOR_122: ColorFormat = ColorFormat("122", "\033[38;5;122m")
    COLOR_123: ColorFormat = ColorFormat("123", "\033[38;5;123m")
    COLOR_124: ColorFormat = ColorFormat("124", "\033[38;5;124m")
    COLOR_125: ColorFormat = ColorFormat("125", "\033[38;5;125m")
    COLOR_126: ColorFormat = ColorFormat("126", "\033[38;5;126m")
    COLOR_127: ColorFormat = ColorFormat("127", "\033[38;5;127m")
    COLOR_128: ColorFormat = ColorFormat("128", "\033[38;5;128m")
    COLOR_129: ColorFormat = ColorFormat("129", "\033[38;5;129m")
    COLOR_130: ColorFormat = ColorFormat("130", "\033[38;5;130m")
    COLOR_131: ColorFormat = ColorFormat("131", "\033[38;5;131m")
    COLOR_132: ColorFormat = ColorFormat("132", "\033[38;5;132m")
    COLOR_133: ColorFormat = ColorFormat("133", "\033[38;5;133m")
    COLOR_134: ColorFormat = ColorFormat("134", "\033[38;5;134m")
    COLOR_135: ColorFormat = ColorFormat("135", "\033[38;5;135m")
    COLOR_136: ColorFormat = ColorFormat("136", "\033[38;5;136m")
    COLOR_137: ColorFormat = ColorFormat("137", "\033[38;5;137m")
    COLOR_138: ColorFormat = ColorFormat("138", "\033[38;5;138m")
    COLOR_139: ColorFormat = ColorFormat("139", "\033[38;5;139m")
    COLOR_140: ColorFormat = ColorFormat("140", "\033[38;5;140m")
    COLOR_141: ColorFormat = ColorFormat("141", "\033[38;5;141m")
    COLOR_142: ColorFormat = ColorFormat("142", "\033[38;5;142m")
    COLOR_143: ColorFormat = ColorFormat("143", "\033[38;5;143m")
    COLOR_144: ColorFormat = ColorFormat("144", "\033[38;5;144m")
    COLOR_145: ColorFormat = ColorFormat("145", "\033[38;5;145m")
    COLOR_146: ColorFormat = ColorFormat("146", "\033[38;5;146m")
    COLOR_147: ColorFormat = ColorFormat("147", "\033[38;5;147m")
    COLOR_148: ColorFormat = ColorFormat("148", "\033[38;5;148m")
    COLOR_149: ColorFormat = ColorFormat("149", "\033[38;5;149m")
    COLOR_150: ColorFormat = ColorFormat("150", "\033[38;5;150m")
    COLOR_151: ColorFormat = ColorFormat("151", "\033[38;5;151m")
    COLOR_152: ColorFormat = ColorFormat("152", "\033[38;5;152m")
    COLOR_153: ColorFormat = ColorFormat("153", "\033[38;5;153m")
    COLOR_154: ColorFormat = ColorFormat("154", "\033[38;5;154m")
    COLOR_155: ColorFormat = ColorFormat("155", "\033[38;5;155m")
    COLOR_156: ColorFormat = ColorFormat("156", "\033[38;5;156m")
    COLOR_157: ColorFormat = ColorFormat("157", "\033[38;5;157m")
    COLOR_158: ColorFormat = ColorFormat("158", "\033[38;5;158m")
    COLOR_159: ColorFormat = ColorFormat("159", "\033[38;5;159m")
    COLOR_160: ColorFormat = ColorFormat("160", "\033[38;5;160m")
    COLOR_161: ColorFormat = ColorFormat("161", "\033[38;5;161m")
    COLOR_162: ColorFormat = ColorFormat("162", "\033[38;5;162m")
    COLOR_163: ColorFormat = ColorFormat("163", "\033[38;5;163m")
    COLOR_164: ColorFormat = ColorFormat("164", "\033[38;5;164m")
    COLOR_165: ColorFormat = ColorFormat("165", "\033[38;5;165m")
    COLOR_166: ColorFormat = ColorFormat("166", "\033[38;5;166m")
    COLOR_167: ColorFormat = ColorFormat("167", "\033[38;5;167m")
    COLOR_168: ColorFormat = ColorFormat("168", "\033[38;5;168m")
    COLOR_169: ColorFormat = ColorFormat("169", "\033[38;5;169m")
    COLOR_170: ColorFormat = ColorFormat("170", "\033[38;5;170m")
    COLOR_171: ColorFormat = ColorFormat("171", "\033[38;5;171m")
    COLOR_172: ColorFormat = ColorFormat("172", "\033[38;5;172m")
    COLOR_173: ColorFormat = ColorFormat("173", "\033[38;5;173m")
    COLOR_174: ColorFormat = ColorFormat("174", "\033[38;5;174m")
    COLOR_175: ColorFormat = ColorFormat("175", "\033[38;5;175m")
    COLOR_176: ColorFormat = ColorFormat("176", "\033[38;5;176m")
    COLOR_177: ColorFormat = ColorFormat("177", "\033[38;5;177m")
    COLOR_178: ColorFormat = ColorFormat("178", "\033[38;5;178m")
    COLOR_179: ColorFormat = ColorFormat("179", "\033[38;5;179m")
    COLOR_180: ColorFormat = ColorFormat("180", "\033[38;5;180m")
    COLOR_181: ColorFormat = ColorFormat("181", "\033[38;5;181m")
    COLOR_182: ColorFormat = ColorFormat("182", "\033[38;5;182m")
    COLOR_183: ColorFormat = ColorFormat("183", "\033[38;5;183m")
    COLOR_184: ColorFormat = ColorFormat("184", "\033[38;5;184m")
    COLOR_185: ColorFormat = ColorFormat("185", "\033[38;5;185m")
    COLOR_186: ColorFormat = ColorFormat("186", "\033[38;5;186m")
    COLOR_187: ColorFormat = ColorFormat("187", "\033[38;5;187m")
    COLOR_188: ColorFormat = ColorFormat("188", "\033[38;5;188m")
    COLOR_189: ColorFormat = ColorFormat("189", "\033[38;5;189m")
    COLOR_190: ColorFormat = ColorFormat("190", "\033[38;5;190m")
    COLOR_191: ColorFormat = ColorFormat("191", "\033[38;5;191m")
    COLOR_192: ColorFormat = ColorFormat("192", "\033[38;5;192m")
    COLOR_193: ColorFormat = ColorFormat("193", "\033[38;5;193m")
    COLOR_194: ColorFormat = ColorFormat("194", "\033[38;5;194m")
    COLOR_195: ColorFormat = ColorFormat("195", "\033[38;5;195m")
    COLOR_196: ColorFormat = ColorFormat("196", "\033[38;5;196m")
    COLOR_197: ColorFormat = ColorFormat("197", "\033[38;5;197m")
    COLOR_198: ColorFormat = ColorFormat("198", "\033[38;5;198m")
    COLOR_199: ColorFormat = ColorFormat("199", "\033[38;5;199m")
    COLOR_200: ColorFormat = ColorFormat("200", "\033[38;5;200m")
    COLOR_201: ColorFormat = ColorFormat("201", "\033[38;5;201m")
    COLOR_202: ColorFormat = ColorFormat("202", "\033[38;5;202m")
    COLOR_203: ColorFormat = ColorFormat("203", "\033[38;5;203m")
    COLOR_204: ColorFormat = ColorFormat("204", "\033[38;5;204m")
    COLOR_205: ColorFormat = ColorFormat("205", "\033[38;5;205m")
    COLOR_206: ColorFormat = ColorFormat("206", "\033[38;5;206m")
    COLOR_207: ColorFormat = ColorFormat("207", "\033[38;5;207m")
    COLOR_208: ColorFormat = ColorFormat("208", "\033[38;5;208m")
    COLOR_209: ColorFormat = ColorFormat("209", "\033[38;5;209m")
    COLOR_210: ColorFormat = ColorFormat("210", "\033[38;5;210m")
    COLOR_211: ColorFormat = ColorFormat("211", "\033[38;5;211m")
    COLOR_212: ColorFormat = ColorFormat("212", "\033[38;5;212m")
    COLOR_213: ColorFormat = ColorFormat("213", "\033[38;5;213m")
    COLOR_214: ColorFormat = ColorFormat("214", "\033[38;5;214m")
    COLOR_215: ColorFormat = ColorFormat("215", "\033[38;5;215m")
    COLOR_216: ColorFormat = ColorFormat("216", "\033[38;5;216m")
    COLOR_217: ColorFormat = ColorFormat("217", "\033[38;5;217m")
    COLOR_218: ColorFormat = ColorFormat("218", "\033[38;5;218m")
    COLOR_219: ColorFormat = ColorFormat("219", "\033[38;5;219m")
    COLOR_220: ColorFormat = ColorFormat("220", "\033[38;5;220m")
    COLOR_221: ColorFormat = ColorFormat("221", "\033[38;5;221m")
    COLOR_222: ColorFormat = ColorFormat("222", "\033[38;5;222m")
    COLOR_223: ColorFormat = ColorFormat("223", "\033[38;5;223m")
    COLOR_224: ColorFormat = ColorFormat("224", "\033[38;5;224m")
    COLOR_225: ColorFormat = ColorFormat("225", "\033[38;5;225m")
    COLOR_226: ColorFormat = ColorFormat("226", "\033[38;5;226m")
    COLOR_227: ColorFormat = ColorFormat("227", "\033[38;5;227m")
    COLOR_228: ColorFormat = ColorFormat("228", "\033[38;5;228m")
    COLOR_229: ColorFormat = ColorFormat("229", "\033[38;5;229m")
    COLOR_230: ColorFormat = ColorFormat("230", "\033[38;5;230m")
    COLOR_231: ColorFormat = ColorFormat("231", "\033[38;5;231m")

    @classmethod
    def get_ansi_by_name(cls, color_name: str) -> str:
        """
        Retrieve the ANSI escape code associated with a specific color name.

        Args:
            color_name: The string representation of the target color.

        Returns:
            The corresponding ANSI string, or the reset code if not found.
        """
        for attr in dir(cls):
            value = getattr(cls, attr)
            if isinstance(value, ColorFormat):
                if value.name == color_name.lower():
                    return value.ansi
        return cls.RESET.ansi

    @classmethod
    def rainbow(cls, text: str) -> str:
        """
        Apply a repeating rainbow color sequence to the given text string.

        Args:
            text: The plain text to be formatted.

        Returns:
            The text interspersed with ANSI color codes.
        """
        palette = [
            "\033[91m",
            "\033[38;5;208m",
            "\033[93m",
            "\033[92m",
            "\033[94m",
            "\033[38;5;177m",
        ]
        result = "".join(
            f"{palette[i % len(palette)]}{char}" for i, char in enumerate(text)
        )
        return f"{result}{cls.RESET.ansi}"

    @classmethod
    def bold(cls, text: str) -> str:
        """
        Wrap the provided text with ANSI bold formatting codes.

        Args:
            text: The plain text to be formatted.

        Returns:
            The bolded text string.
        """
        bold: str = "\033[1m"
        reset: str = "\033[0m"
        return f"{bold}{text}{reset}"

    @classmethod
    def apply(
        cls,
        style: str | None = None,
        color_name: str = "reset",
        text: str = "",
    ) -> str:
        """
        Apply a specific color and optional styling to a text string.

        Args:
            style: An optional formatting style (e.g., "bold").
            color_name: The target color name (e.g., "rainbow", "red").
            text: The text to be styled.

        Returns:
            The fully formatted string containing appropriate ANSI codes.
        """
        if color_name.lower() == "rainbow":
            result = cls.rainbow(text)
        else:
            ansi = cls.get_ansi_by_name(color_name)
            result = f"{ansi}{text}{cls.RESET.ansi}"

        if style == "bold":
            result = cls.bold(result)

        return result


# ----------------------------------------------------------------------------
#  Specific messages formatting
# ----------------------------------------------------------------------------

def error(text: str) -> None:
    """
    Format and print an error message to the terminal in bold magenta.

    Args:
        text: The error message content.
    """
    print(TerminalFormatter.apply("bold", "magenta", f">>> ERROR! {text}"))


def warning(text: str) -> None:
    """
    Format and print a warning message to the terminal in bold yellow.

    Args:
        text: The warning message content.
    """
    print(TerminalFormatter.apply("bold", "yellow", f">>> WARNING! {text}"))
