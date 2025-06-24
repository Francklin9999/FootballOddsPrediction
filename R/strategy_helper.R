library(shiny)
library(jsonlite)
library(httr)

load_strategy_choices <- function() {
  fromJSON("strategy_choices.json")
}

render_strategy_inputs <- function(strategy_choices, strategy) {
  params <- strategy_choices$strategies_params[[strategy]]
  
  input_elements <- lapply(params, function(param) {
    if (param == "team") {
      return(selectInput(paste0("input_", param), paste("Select a", param), choices = strategy_choices$teams))
    } else if (param == "year") {
      return(selectInput(paste0("input_", param), paste("Select a", param), choices = strategy_choices$years))
    } else if (param == "bankroll") {
      return(numericInput(paste0("input_", param), "Enter bankroll", value = 1000))
    } else if (param == "base_bet") {
      return(numericInput(paste0("input_", param), "Enter base bet", value = 50))
    } else if (param == "sequence") {
      return(textInput(paste0("input_", param), "Enter sequence (comma separated)", value = "1,2,3"))
    } else if (param == "bet_amount") {
      return(numericInput(paste0("input_", param), "Enter bet amount", value = 100))
    } else if (param == "percentage") {
      return(numericInput(paste0("input_", param), "Enter percentage", value = 0.05, min = 0, max = 1))
    }
  })
  
  return(input_elements)
}

fetch_strategy_data <- function(input, params) {
  query_params <- list(
    selected_strategy = input$select_strategy,
    selected_strategy_team = input$select_strategy_team,
    selected_strategy_year = input$select_strategy_year
  )
  
  for (param in params) {
    dynamic_input_id <- paste0("input_", param)
    if (!is.null(input[[dynamic_input_id]])) {
      query_params[[param]] <- input[[dynamic_input_id]]
    }
  }
  
  response <- GET(
    url = "http://127.0.0.1:5000/run_strategy",
    query = query_params
  )
  
  return(response)
}

plot_time_money <- function(history) {
  history_df <- data.frame(
    Time = as.numeric(names(history)),
    Money = unlist(history)
  )
  
  plot(history_df$Time, history_df$Money, 
       type = "o", 
       col = "blue", 
       pch = 16, 
       lwd = 2, 
       cex = 1.5, 
       xlab = "Time (Weeks)", 
       ylab = "Money ($)", 
       main = "Bankroll over the season", 
       col.main = "darkblue", 
       col.lab = "darkgreen", 
       col.axis = "gray20", 
       las = 1,
       xaxt = "n", yaxt = "n",
       bty = "l")
  
  axis(1, at = seq(min(history_df$Time), max(history_df$Time), by = 10), 
       labels = seq(min(history_df$Time), max(history_df$Time), by = 10), col = "gray20")
  axis(2, at = seq(min(history_df$Money), max(history_df$Money), by = 100), 
       labels = seq(min(history_df$Money), max(history_df$Money), by = 100), col = "gray20")
  
  grid(col = "lightgray", lwd = 1)
  
  lines(smooth.spline(history_df$Time, history_df$Money), col = "darkred", lwd = 2, lty = 2)
}

handle_response_and_plot <- function(response, output) {
  if (status_code(response) == 200) {
    response_content <- fromJSON(content(response, "text", encoding = "UTF-8"))
    
    output$response <- renderText({
      if (!is.null(response_content$bankroll) && !is.null(response_content$history)) {
        paste("Final Bankroll: ", response_content$bankroll)
      } else {
        "No message in response."
      }
    })
    
    output$time_money_plot <- renderPlot({
      if (!is.null(response_content$history) && length(response_content$history) > 0) {
        plot_time_money(response_content$history)
      } else {
        plot(0, type = "n", xlab = "Time", ylab = "Money", main = "No Data Available")
      }
    })
  } else {
    output$response <- renderText({
      paste("Error:", status_code(response), "- Unable to retrieve data.")
    })
  }
}

