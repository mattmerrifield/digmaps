class Evidence:
    """
    Constants to quantitatively describe how certain we are that a site
    contains evidence for a certain tag.
    """

    VERY_CLEAR = 100
    CLEAR = 50
    TYPICAL = 0
    UNCLEAR = -50
    VERY_UNCLEAR = -100

    CHOICES = (
        (VERY_CLEAR, "Very clear evidence"),
        (CLEAR, "Clear evidence"),
        (TYPICAL, "Typical evidence"),
        (UNCLEAR, "Unclear evidence"),
        (VERY_UNCLEAR, "Very unclear evidence"),
    )
