library(tidyverse)

data <- read_csv("forestfires.csv")

head(data)

unique(data$month)
unique(data$day)


data <- data %>%
  mutate(
    month_category = factor(
      month,
      levels=c("jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep",
               "oct", "nov", "dec")),
    day_category = factor(
      day,
      levels=c("mon", "tue", "wed", "thu", "fri", "sat", "sun")
    )
  )

monthly_forest_fires <- data %>%
  group_by(month_category) %>%
  summarise(
    number_of_fires = n()
  )

forest_fires_by_day_of_week <- data %>%
  group_by(day_category) %>%
  summarise(
    number_of_fires = n()
  )

monthly_forest_fires %>%
  ggplot(aes(x=month_category, y=number_of_fires, group=1)) +
  theme(panel.background = element_rect(fill="white")) + 
  geom_line() +
  labs(
    title="Frequency of Forest Fires By Month",
    x="Month",
    y="Number of Fires"
  )
  
forest_fires_by_day_of_week %>%
  ggplot(aes(x=day_category, y=number_of_fires)) +
  theme(panel.background = element_rect(fill="white")) + 
  geom_col(fill="blue") +
  labs(
    title="Frequency of Forest Fires By Day",
    x="Day",
    y="Number of Fires"
  )


data_long_format <- data %>%
  pivot_longer(
    cols = c("FFMC", "DMC", "DC", "ISI", "temp", "RH", "wind", "rain"),
    names_to = "column",
    values_to = "value"
  )

data_long_format %>%
  ggplot(aes(x=month_category, y=value)) +
  geom_boxplot() +
  facet_wrap(vars(column), scales="free_y") +
  labs(
    title="Fire Variable Changes Over Month",
    x="Month",
    y="Scale"
  )

data_long_format %>%
  ggplot(aes(x=value, y=area)) +
  geom_point() +
  facet_wrap(vars(column), scales="free_x") +
  labs(
    title="Fire Variable Changes By Impact To Area",
    x="Variables",
    y="Area (Number of Hectares)"
  )

data %>%
  ggplot(aes(x=area, )) +
  geom_histogram()

data_long_format %>%
  filter(area != 0, area <= 150) %>%
  ggplot(aes(x=value, y=area)) +
  geom_point() +
  facet_wrap(vars(column), scales="free_x") +
  labs(
    title="Fire Variable Changes By Impact To Area",
    x="Variables",
    y="Area (Number of Hectares)"
  )
