library(shiny)
library(jsonlite)
library(ggplot2)
library(plotly)
library(readr)

source("strategy_helper.R")

function(input, output, session) {
  strategy_choices <- load_strategy_choices()
  
  params <- reactiveVal(NULL)
  
  observeEvent(input$select_strategy, {
    strategy <- input$select_strategy
    
    params(strategy_choices$strategies_params[[strategy]])
    
    output$strategy_dynamic_inputs <- renderUI({
      param_list <- params()
      
      if (length(param_list) > 0) {
        input_elements <- render_strategy_inputs(strategy_choices, strategy)
        do.call(tagList, input_elements)
      }
    })
  })
  
  observeEvent(input$strategy_btn, {
    param_list <- params()
    
    response <- fetch_strategy_data(input, param_list)
    
    handle_response_and_plot(response, output)
  })
  
    observeEvent(input$select_strategy, {
    strategy <- input$select_strategy
    
    params(strategy_choices$strategies_params[[strategy]])
    
    output$strategy_dynamic_inputs <- renderUI({
      param_list <- params()
      
      if (length(param_list) > 0) {
        input_elements <- render_strategy_inputs(strategy_choices, strategy)
        do.call(tagList, input_elements)
      }
    })
  })
  
  observeEvent(input$strategy_btn, {
    param_list <- params()
    
    response <- fetch_strategy_data(input, param_list)
    
    handle_response_and_plot(response, output)
  })
  
  observeEvent(input$submit_arbitrage, {
    req(input$odd1, input$odd2)
    response <- GET(
      url = "http://127.0.0.1:5000/isArbitrage",
      query = list(odd1 = input$odd1, odd2 = input$odd2)
    )
    result <- content(response, "text", encoding = "UTF-8")
    output$arbitrage_result <- renderText({ result })
  })
  
  observeEvent(input$submit_arbitrage_calc, {
    req(input$calc_odd1, input$calc_odd2)
    response <- GET(
      url = "http://127.0.0.1:5000/arbitrage_calculator",
      query = list(odd1 = input$calc_odd1, odd2 = input$calc_odd2)
    )
    result <- fromJSON(content(response, "text", encoding = "UTF-8"))
    
    if(result$is_arbitrage == "TRUE") {
      output$arbitrage_stakes <- renderText({
        paste(
          "Arbitrage Opportunity Found.", "\n",
          "Percentage to put on Team 1:", round(result$stake1 * 100, 2), "%", "\n",
          "Percentage to put on Team 2:", round(result$stake2 * 100, 2), "%", "\n",
          "Expected Profit:", round(result$profit * 100, 2), "%", "\n"
        )
      })
    } else {
      output$arbitrage_stakes <- renderText({
        paste("No Arbitrage Opportunity Found.")
      })
    }
  })
  
  observeEvent(input$submit_ev, {
    req(input$ev_odd, input$ev_prob, input$ev_stake)
    response <- GET(
      url = "http://127.0.0.1:5000/ev_calculator",
      query = list(odds = input$ev_odd, probability = input$ev_prob, stake = input$ev_stake)
    )
    result <- fromJSON(content(response, "text", encoding = "UTF-8"))
    output$ev_result <- renderText({
      if (result$is_profitable) {
        paste(
          "Expected Value", result$expected_value, "\n", 
          "EV Opportunity found"
          )
      } else {
        paste(
          "Expected Value", result$expected_value, "\n", 
          "No EV Opportunity"
          )
      }
    })
  })
  
  observeEvent(input$submit_predict_odds, {
    data <- list(
      HomeTeam = input$predict_odds_team_home,
      AwayTeam = input$predict_odds_team_away,
      HomeLastMatch = input$HomeLastMatch,
      AwayLastMatch = input$AwayLastMatch,
      HomeAvgGoals = input$HomeAvgGoals,
      AwayAvgGoals = input$AwayAvgGoals,
      HomeWinStreak = input$HomeWinStreak,
      AwayWinStreak = input$AwayWinStreak,
      HomeAvgConceded = input$HomeAvgConceded,
      AwayAvgConceded = input$AwayAvgConceded,
      HomeGoalDiffAvg = input$HomeGoalDiffAvg,
      AwayGoalDiffAvg = input$AwayGoalDiffAvg
    )
    
    response <- GET(
      "http://127.0.0.1:5000/predict_odds", 
      query = data
      )
    if (status_code(response) == 200) {
      result <- fromJSON(content(response, "text", encoding = "UTF-8"))
      
      output$win_pred <- renderText({ paste("Win Prediction:", result$win_pred) })
      output$over25_odds_pred <- renderText({ paste("Over 2.5 Odds Prediction:", result$over25_odds_pred) })
      output$over25_pred <- renderText({ paste("Over 2.5 Prediction:", result$over25_pred) })
      output$home_odds_pred <- renderText({ paste("Home Odds Prediction:", result$home_odds_pred) })
      output$away_odds_pred <- renderText({ paste("Away Odds Prediction:", result$away_odds_pred) })
      
    } else {
      output$win_pred <- renderText("Error: Could not get prediction.")
      output$over25_odds_pred <- renderText("")
      output$over25_pred <- renderText("")
      output$home_odds_pred <- renderText("")
      output$away_odds_pred <- renderText("")
    }
  })
  
  observeEvent(input$submit_simulation, {
    data <- list(
      HomeTeam = input$homeTeam,
      AwayTeam = input$awayTeam,
      HomeOdds = input$homeOdds,
      DrawOdds = input$drawOdds,
      AwayOdds = input$awayOdds,
      SelectedSimluationYear = input$selected_simulation_year
    )
    
    response <- GET(
      url = "http://127.0.0.1:5000/run_simulation",
      query = data
    )
    
    if (status_code(response) == 200) {
      result <- fromJSON(content(response, "text", encoding = "UTF-8"))
      
      output$simulation_result <- renderText({
        paste(
          "Home Win Probability: ", result$home_win_prob, "\n",
          "Draw Probability: ", result$draw_prob, "\n",
          "Away Win Probability: ", result$away_win_prob, "\n",
          "Over 2.5 Goals Probability: ", result$over_2_5_prob, "\n",
          "Adjusted Home Win Odds: ", result$adjusted_home_win_odds, "\n",
          "Adjusted Draw Odds: ", result$adjusted_draw_odds, "\n",
          "Adjusted Away Win Odds: ", result$adjusted_away_win_odds
        )
      })
      
      odds_data <- c(
        result$adjusted_home_win_odds, 
        result$adjusted_draw_odds, 
        result$adjusted_away_win_odds
      )
      
      odds_labels <- c(
        "adjusted_home_win_odds", 
        "adjusted_draw_odds", 
        "adjusted_away_win_odds"
      )
      
      probability_data <- c(
        result$home_win_prob,
        result$draw_prob,
        result$away_win_prob,
        result$over_2_5_prob
      )
      
      probability_labels <- c(
        "Home Win Probability", 
        "Draw Probability", 
        "Away Win Probability", 
        "Over 2.5 Probability"
      )
      
      output$odds_histogram <- renderPlot({
        par(mfrow = c(1, 2))
        
        barplot(probability_data, 
                main = "Probability Distribution", 
                ylab = "Probability", 
                col = "lightgreen", 
                names.arg = probability_labels,
                las = 2,
                border = "white"
        )
        
        barplot(odds_data, 
                main = "Adjusted Odds Distribution", 
                ylab = "Odds", 
                col = "skyblue", 
                names.arg = odds_labels,
                las = 2,
                border = "white"
        )
      })
      
      
    } else {
      output$simulation_result <- renderText({
        paste("Error:", status_code(response), "- Unable to retrieve data.")
      })
    }
  })
  
  observeEvent(input$submit_predict_odds, {
    query_params <- list(
      selected_strategy_team = input$select_strategy_team_all,
      selected_strategy_year = input$select_strategy_year_all,
      bankroll = input$select_strategy_bankroll_all,
      base_bet = input$select_strategy_bet_all,
      bet_amount = input$select_strategy_bet_all,
      percentage = input$select_strategy_percentage_all
    )
    
    response <- GET(
      url = "http://127.0.0.1:5000/run_strategy_all",
      query = query_params
    )
    
    result <- fromJSON(content(response, "text", encoding = "UTF-8"))
    
    output$strategy_all_bankroll_plot <- renderPlotly({
      req(result)
      
      strategies <- names(result$result)
      bankrolls <- sapply(strategies, function(strategy) result$result[[strategy]]$bankroll)
      
      plot_ly(
        x = strategies,
        y = bankrolls,
        type = 'bar',
        marker = list(color = 'skyblue'),
        text = bankrolls,
        hoverinfo = 'text'
      ) %>%
        layout(
          title = "Bankroll by Strategy",
          xaxis = list(title = "Strategy"),
          yaxis = list(title = "Bankroll")
        )
    })

    output$strategy_all_history_plot <- renderPlotly({
      req(result)
      
      strategies <- names(result$result)
      
      plot <- plot_ly()
      
      for (strategy in strategies) {
        history <- result$result[[strategy]]$history
        history_values <- unlist(history)
        
        plot <- plot %>%
          add_trace(
            x = 1:length(history_values),
            y = history_values,
            type = 'scatter',
            mode = 'lines+markers',
            name = strategy
          )
      }
      
      plot %>%
        layout(
          title = "History of Strategies",
          xaxis = list(title = "Time"),
          yaxis = list(title = "Amount")
        )
    })
  })
  
  data_values <- reactiveVal(NULL)
  
  observeEvent(input$submit_csv_data, {
    req(input$inputFile)
    
    response <- POST(
      "http://127.0.0.1:5000/process_csv",
      body = list(file = upload_file(input$inputFile$datapath)),
      encode = "multipart"
    )
    
    if (status_code(response) == 200) {
      response_data <- fromJSON(content(response, "text", encoding = "UTF-8"))
      
      csv_content <- response_data$csv_content
      json_content <- response_data$json_content
      
      tryCatch({
        csv_data <- read.csv(text = csv_content, stringsAsFactors = FALSE, check.names = FALSE)
      }, error = function(e) {
        csv_data <- data.frame(Content = csv_content)
      })
      
      tryCatch({
        json_data <- fromJSON(json_content, flatten = TRUE)
      }, error = function(e) {
        json_data <- list(Error = "Failed to parse JSON content")
      })
      
      data_values(list(csv = csv_data, json = json_data))
    } else {
      showNotification("Failed to process CSV file", type = "error")
      data_values(NULL)
    }
  })
  
  output$downloadCSV <- downloadHandler(
    filename = function() {
      paste("processed-", input$inputFile$name, sep = "")
    },
    content = function(file) {
      req(data_values())
      write.csv(data_values()$csv, file, row.names = FALSE)
    }
  )
  
  output$downloadJSON <- downloadHandler(
    filename = function() {
      paste("processed-", input$inputFile$name, ".json", sep = "")
    },
    content = function(file) {
      req(data_values())
      jsonlite::write_json(data_values()$json, path = file, pretty = TRUE)
    }
  )
}
