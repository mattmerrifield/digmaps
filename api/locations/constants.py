class Evidence:
    """
    Constants to quantitatively describe how certain we are that a site
    contains evidence for a certain tag.
    """

    VERY_CLEAR = "E100"
    CLEAR = "E50"
    TYPICAL = "E0"
    UNCLEAR = "E-50"
    VERY_UNCLEAR = "E-100"

    CHOICES = (
        (VERY_CLEAR, "Very clear evidence"),
        (CLEAR, "Clear evidence"),
        (TYPICAL, "Typical evidence"),
        (UNCLEAR, "Unclear evidence"),
        (VERY_UNCLEAR, "Very unclear evidence"),
    )
