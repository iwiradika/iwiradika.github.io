# Palet dan tema visual iwiradika.github.io untuk ggplot2
iw_palette <- c(
  navy = "#032454", gold = "#FCC209", silver = "#E7EAEE",
  background = "#F9FAFB", paper = "#FFFFFF", muted = "#4A5F7E",
  border = "#DDE1E8", positive = "#2E7D32", warning = "#F57F17",
  negative = "#C62828"
)

scale_colour_iw <- function(...) {
  ggplot2::scale_colour_manual(values = unname(iw_palette[c("navy", "gold", "muted", "positive", "warning", "negative")]), ...)
}

scale_fill_iw <- function(...) {
  ggplot2::scale_fill_manual(values = unname(iw_palette[c("navy", "gold", "silver", "positive", "warning", "negative")]), ...)
}

theme_iw <- function(base_size = 11, base_family = "Inter") {
  ggplot2::theme_minimal(base_size = base_size, base_family = base_family) +
    ggplot2::theme(
      plot.background = ggplot2::element_rect(fill = iw_palette[["background"]], colour = NA),
      panel.background = ggplot2::element_rect(fill = iw_palette[["background"]], colour = NA),
      plot.title = ggplot2::element_text(family = "Playfair Display", face = "bold", colour = iw_palette[["navy"]], size = ggplot2::rel(1.45)),
      plot.subtitle = ggplot2::element_text(colour = iw_palette[["muted"]], margin = ggplot2::margin(b = 12)),
      plot.caption = ggplot2::element_text(colour = iw_palette[["muted"]], hjust = 0),
      axis.title = ggplot2::element_text(colour = iw_palette[["navy"]], face = "bold"),
      axis.text = ggplot2::element_text(colour = iw_palette[["muted"]]),
      panel.grid.major.x = ggplot2::element_blank(),
      panel.grid.minor = ggplot2::element_blank(),
      panel.grid.major.y = ggplot2::element_line(colour = iw_palette[["border"]], linewidth = 0.35),
      legend.position = "top",
      legend.title = ggplot2::element_blank()
    )
}

# Contoh:
# ggplot(data, aes(x, y, fill = group)) +
#   geom_col(width = .68) +
#   scale_fill_iw() +
#   theme_iw()
