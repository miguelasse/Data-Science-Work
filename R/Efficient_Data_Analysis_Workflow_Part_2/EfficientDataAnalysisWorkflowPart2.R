library(readr)
library(tidyverse)
library(stringr)
library(dplyr)
library(lubridate)

data <- read_csv("sales2019.csv")

unique(data)

dim(data)

column_names <- colnames(data)
print(column_names)

colSums(is.na(data))

clean_reviews <- data %>%
  dplyr::filter(
    !is.na(user_submitted_review)
  )

average_number_of_books_purchased <- clean_reviews %>%
  filter(
    !is.na(total_purchased)
  ) %>%
  pull(total_purchased) %>%
  mean()

clean_reviews <- clean_reviews %>%
  mutate(
    imputed_total_purchased
      = if_else(
        is.na(total_purchased),
        average_number_of_books_purchased,
        total_purchased)
  )

determine_positive_review <- function(review) {
  review_positive = case_when(
    str_detect(review, "Awesome") ~ TRUE,
    str_detect(review, "Never") ~ TRUE,
    str_detect(review, "OK") ~ TRUE,
    str_detect(review, "a lot") ~ TRUE,
    TRUE ~ FALSE # Set any reviews outside of the above to FALSE
  )
}

clean_reviews <- clean_reviews %>%
  mutate(
    is_positive_review = determine_positive_review(user_submitted_review)
  )

clean_reviews$date <- mdy(clean_reviews$date)

clean_reviews <- clean_reviews %>%
  mutate(
    sale_after_program_start = clean_reviews$date > mdy("07/01/2019")
  )

book_sales_review <- clean_reviews %>%
  group_by(sale_after_program_start) %>%
  summarise(
    books_purchased = sum(imputed_total_purchased))

book_sales_review_by_title <- clean_reviews %>%
  group_by(sale_after_program_start, title) %>%
  summarise(
    books_purchased = sum(imputed_total_purchased)) %>%
  arrange(title, sale_after_program_start)

book_sales_review_by_customer_type <- clean_reviews %>%
  group_by(sale_after_program_start, customer_type) %>%
  summarise(
    books_purchased = sum(imputed_total_purchased)) %>%
  arrange(customer_type, sale_after_program_start)

positive_reviews_after_program <- clean_reviews %>%
  group_by(sale_after_program_start) %>%
  summarise(
    total_positive_reviews = sum(is_positive_review)) %>%
  arrange(total_positive_reviews, sale_after_program_start)
