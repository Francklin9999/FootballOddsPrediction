library(ggplot2)

plot_time_money <- function(data) {
  df <- data.frame(
    time = as.numeric(names(data)),
    money = as.numeric(data)
  )
  
  ggplot(df, aes(x = time, y = money)) +
    geom_line() +
    geom_point() +
    labs(x = "Time", y = "Money", title = "Bankroll over The Season") +
    theme_minimal()
}
