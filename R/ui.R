library(shiny)
library(shinydashboard)
library(jsonlite)
library(plotly)

strategy_choices <- fromJSON("strategy_choices.json")
data_json <- fromJSON("data.json")

dashboardPage(
  dashboardHeader(title = "Sport  Betting Predictor App", 
                  titleWidth = 650,
                  tags$li(class="dropdown", tags$a(href="https://www.football-data.co.uk/data.php", icon=icon("database"), "Source Data", target="_blank"))
                  ),
  dashboardSidebar(
    sidebarMenu(
      id = "sidebar",
      menuItem("Analysis", tabName = "data", icon = icon("database")),
      menuItem(text = "Strategies", tabName = "strat", icon=icon("chart-line")),
      menuItem(text = "Simulation", tabName = "sim", icon=icon("map"))
    )
  ),
  dashboardBody(
    tabItems(
      tabItem(
        tabName = "data",
        fluidRow(
          column(
            width = 12,
            tabBox(
              id = "t1", width = 12,
              tabPanel(
                title = "Odds Prediction", 
                icon = icon("chart-line"), 
                h3("Odds Prediction Function"),
                
                fluidRow(
                  column(4, selectInput("predict_odds_team_home", "Select a Home team:", choices = data_json$teams)),
                  column(4, selectInput("predict_odds_team_away", "Select an Away team:", choices = data_json$teams)),
                  column(4, numericInput("HomeLastMatch", "Home Team Time Since Last Match", 1, min = 0, max = 7)),
                  column(4, numericInput("AwayLastMatch", "Away Team Time Since Last Match", 1, min = 0, max = 7)),
                  column(4, numericInput("HomeAvgGoals", "Home Average Goals", 1.5, min = 0, max = 10)),
                  column(4, numericInput("AwayAvgGoals", "Away Average Goals", 1.5, min = 0, max = 10)),
                  column(4, numericInput("HomeWinStreak", "Home Win Streak", 3, min = 0, max = 10)),
                  column(4, numericInput("AwayWinStreak", "Away Win Streak", 2, min = 0, max = 10)),
                  column(4, numericInput("HomeAvgConceded", "Home Average Goals Conceded", 1, min = 0, max = 10)),
                  column(4, numericInput("AwayAvgConceded", "Away Average Goals Conceded", 1, min = 0, max = 10)),
                  column(4, numericInput("HomeGoalDiffAvg", "Home Team Average Goal Difference", 2, min = -10, max = 10)),
                  column(4, numericInput("AwayGoalDiffAvg", "Away Team Average Goal Difference", 2, min = -10, max = 10))
                ),
                
                div(style = "text-align: center;",
                    actionButton("submit_predict_odds", "Get Prediction")
                ),
                
                br(),
                tags$hr(),
                div(style = "text-align: center; font-size: 18px; font-weight: bold;",
                    h4("Prediction Results"),
                    div(style = "margin-top: 10px; color: #2E86C1;",textOutput("win_pred", inline = TRUE)),
                    div(style = "margin-top: 5px; color: #D35400;", textOutput("over25_odds_pred", inline = TRUE)),
                    div(style = "margin-top: 5px; color: #27AE60;", textOutput("over25_pred", inline = TRUE)),
                    div(style = "margin-top: 5px; color: #8E44AD;", textOutput("home_odds_pred", inline = TRUE)),
                    div(style = "margin-top: 5px; color: #C0392B;", textOutput("away_odds_pred", inline = TRUE))
                ),
                tags$hr()
              ),
              
              tabPanel(
                title = "Arbitrage Calculator", 
                icon = icon("calculator"), 
                div(style = "text-align: center;",
                    h3(icon("percent"), "Arbitrage Calculator"),
                    p("Find risk-free betting opportunities by entering the odds for both teams.")
                ),
                
                fluidRow(
                  column(6, numericInput("calc_odd1", strong("Odds for Team 1"), value = 2.00, min = 1, step = 0.01)),
                  column(6, numericInput("calc_odd2", strong("Odds for Team 2"), value = 2.50, min = 1, step = 0.01))
                ),
                
                div(style = "text-align: center; margin-top: 10px;",
                    actionButton("submit_arbitrage_calc", "Calculate Arbitrage Stakes", 
                                 style = "background-color: #27AE60; color: white; font-size: 16px; padding: 10px 20px; border-radius: 8px;")
                ),
                
                br(),
                tags$hr(),
                div(style = "text-align: center; font-size: 18px; color: #E74C3C; font-weight: bold;",
                    textOutput("arbitrage_stakes")
                ),
                tags$hr()
              ),
              
              tabPanel(
                title = "EV Calculator", 
                icon = icon("money-bill-wave"), 
                h3("EV Calculator Function"),
                numericInput("ev_odd", "Enter Odds", value = 2.0, min = 1, step = 0.01),
                numericInput("ev_prob", "Enter Probability", value = 0.5, min = 0, max = 1, step = 0.01),
                numericInput("ev_stake", "Enter Stake", value = 100, min = 1),
                actionButton("submit_ev", "Calculate EV"),
                div(style = "text-align: center; font-size: 18px; color: #E74C3C; font-weight: bold;",
                    textOutput("ev_result")
                ),
              ),
              tabPanel(
                title = "Transform Data", 
                icon = icon("map"), 
                h3("Transform your csv file."),
                fileInput("inputFile", "Choose CSV File", accept = ".csv"),
                actionButton("submit_csv_data", "Transform"),
                
                downloadButton("downloadCSV", "Download CSV"),
                downloadButton("downloadJSON", "Download JSON")
              )
            )
          )
        )
      ),
      tabItem(tabName = "strat",
              tabBox(id="t2", width = 12,
                     tabPanel("Input", icon = icon("database"), h4("English Premier League Strategy betting"), 
                              selectInput("select_strategy", "Select a strategy:", choices = strategy_choices$strategies),
                              selectInput("select_strategy_team", "Select a team:", choices = strategy_choices$teams),
                              selectInput("select_strategy_year", "Select a year:", choices = strategy_choices$years),
                              uiOutput("strategy_dynamic_inputs"),
                              actionButton("strategy_btn", "Submit"),
                              ),
                     tabPanel("Results",
                              icon = icon("chart-line"),
                              h3("Strategy Results"),
                              
                              verbatimTextOutput("strategy_result"),
                              
                              textOutput("response"),
                              plotOutput("time_money_plot")
                     ),
                     tabPanel("Compare Strateggy",
                              icon = icon("map"),
                              h3("Compare all Strategies"),
                              fluidRow(
                                column(3, selectInput("select_strategy_team_all", "Select a team:", choices = strategy_choices$teams)),
                                column(3, selectInput("select_strategy_year_all", "Select a year:", choices = strategy_choices$years)),
                                column(3, numericInput("select_strategy_bankroll_all", "Enter bankroll", value = 1000)),
                                column(3, numericInput("select_strategy_bet_all", "Enter base bet", value = 50)),
                                column(3, numericInput("select_strategy_percentage_all", "Enter percentage", value = 0.05, min = 0, max = 1))
                              ),
                              
                              div(style = "text-align: center;",
                                  actionButton("submit_predict_odds", "Get Prediction")
                              ),
                              
                              fluidRow(
                                column(12,
                                       plotlyOutput("strategy_all_bankroll_plot")
                                ),
                                column(12,
                                       plotlyOutput("strategy_all_history_plot")
                                )
                              )
                              
                              )
              )
      ),
        tabItem(
          tabName = "sim",
          fluidRow(
            column(
              width = 12,
              tabBox(
                id = "t1", width = 12,
                
                tabPanel("Simulation Settings",
                         icon = icon("calculator"),
                         h3("Enter Simulation Parameters"),
                         
                         fluidRow(
                           column(4, selectInput("homeTeam", "Select a Home team:", choices = data_json$teams)),
                           column(4, selectInput("awayTeam", "Select an Away team:", choices = data_json$teams)),
                           column(4, numericInput("homeOdds", "Home Odds", 1, min = 0, max = 7)),
                           column(4, numericInput("drawOdds", "Draw Odds", 1, min = 0, max = 7)),
                           column(4, numericInput("awayOdds", "Away Odds", 1.5, min = 0, max = 10)),
                           column(4, selectInput("selected_simulation_year", "Select a year:", choices = strategy_choices$years))
                         ),
                         
                         div(style = "text-align: center;",
                             actionButton("submit_simulation", "Run Simulation")
                         ),
                ),
                
                tabPanel("Results", 
                         icon = icon("chart-line"),
                         h3("Simulation Results"),
                         verbatimTextOutput("simulation_result"),
                         plotOutput("odds_histogram")
                )
              )
            )
          )
        )
      )
    )
)