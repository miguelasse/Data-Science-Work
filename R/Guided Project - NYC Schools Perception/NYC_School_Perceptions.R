library(readr)
library(tidyverse)
library(ggplot2)

combined_school_data <- read_csv("combined_school_data.csv")
masterfile11_gened_final <- read_tsv("masterfile11_gened_final.txt")
masterfile11_d75_final <- read_tsv("masterfile11_d75_final.txt")

gen_ed_cleaned <- masterfile11_gened_final %>%
  filter(schooltype == "High School") %>%
  select(dbn:aca_tot_11)

d75_cleaned <- masterfile11_d75_final %>%
  select(dbn:aca_tot_11)

survey_data <- bind_rows(gen_ed_cleaned, d75_cleaned)
survey_data <- survey_data %>% rename(DBN = dbn)

school_and_survey_data <- combined_school_data %>%
  left_join(survey_data, by="DBN")

school_and_survey_data <- school_and_survey_data %>%
  rename(
    num_of_sat_test_takers = `Num of SAT Test Takers`,
    sat_reading_avg_score = `SAT Critical Reading Avg. Score`,
    sat_math_avg_score = `SAT Math Avg. Score`,
    sat_writing_avg_score = `SAT Writing Avg. Score`,
    ap_test_takers = `AP Test Takers`,
    total_exams_taken = `Total Exams Taken`,
    num_exams_with_scores_3_4_or_5 = `Number of Exams with scores 3 4 or 5`,
    total_cohort = `Total Cohort`
    )

cor_mat <- school_and_survey_data %>%
  select(avg_sat_score, saf_p_11:aca_tot_11) %>%
  cor(use="pairwise.complete.obs")

cor_tib <- cor_mat %>%
  as_tibble(rownames = "variable")

interesting_variables <- cor_tib %>%
  select(variable, avg_sat_score) %>%
  filter(avg_sat_score < -0.25 | avg_sat_score > 0.25)

create_scatter_plot <- function(x, y) {
  ggplot(data = school_and_survey_data) +
    aes_string(x=x, y=y) +
    geom_point(alpha=0.3) +
    theme(panel.background = element_rect(fill = "white"))
}

x_var <- interesting_variables$variable[2:5]
y_var <- "avg_sat_score"

map2(x_var, y_var, create_scatter_plot)


school_and_survey_longer <- school_and_survey_data %>%
  pivot_longer(
    cols = saf_p_11:aca_tot_11,
    names_to = "survey_question",
    values_to = "score"
  )

school_and_survey_longer <- school_and_survey_longer %>%
  mutate(response_type = str_sub(survey_question, 4, 6)) %>%
  mutate(question = str_sub(survey_question, 1, 3))

unique(school_and_survey_longer$question)
school_and_survey_longer <- school_and_survey_longer %>%
  mutate(response_type = ifelse(response_type == "_p_", "parent", 
                                if_else(response_type == "_t_", "teacher",
                                        if_else(response_type == "_s_", "student",
                                                if_else(response_type == "_to", "total", "N/A")))))


school_and_survey_longer <- school_and_survey_longer %>%
  mutate(question = ifelse(question == "saf", "safety & respect", 
                                if_else(question == "com", "communication",
                                        if_else(question == "eng", "engagement",
                                                if_else(question == "aca", "academic expectations", "N/A")))))


school_and_survey_longer %>%
  filter(response_type != "total") %>%
  ggplot(aes(x=question, y=score, fill=response_type)) +
  geom_boxplot()