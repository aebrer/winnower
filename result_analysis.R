library(ggplot2)
library(ggthemes)

mydata = read.csv("results.tsv", stringsAsFactors=F, sep = "\t", header=F)
head(mydata)
names(mydata) = c("rm1","rm2","liked", "score", "name", "age", "id", "rm")
mydata$rm = NULL
mydata$rm1 = NULL
mydata$rm2 = NULL
mydata$liked[mydata$liked == "like"] = 1
mydata$liked[mydata$liked == "super"] = 1
mydata$liked[mydata$liked == "dislike"] = 0
mydata$liked = as.numeric(mydata$liked)

ggplot(mydata) +
  geom_jitter(aes(x=age, y=score), alpha = 0.1) +
  geom_tufteboxplot(aes(x=age, y=score, group=age)) +
  ylim(c(0,110)) +
  theme_tufte() +
  scale_y_continuous(breaks = c(0,4.05,10,15,20,30,50,75,100)) +
  geom_hline(yintercept = 6)

head(mydata[order(mydata$score, decreasing=T),], 10)
length(mydata$name)

library(dplyr)

name_data = mydata %>%
  group_by(name) %>%
  summarise(length(score), mean(score), median(score), mean(liked))

name_data = name_data[name_data$`length(score)` > 5,]
head(name_data[order(name_data$`mean(liked)`, decreasing=T),], 10)


age_data = mydata %>%
  group_by(age) %>%
  summarise(length(score), length(score[score > 6]), length(score[score > 6]) / length(score), mean(score), median(score), mean(liked))

age_data

head(age_data[order(age_data$`mean(liked)`, decreasing=T),], 10)
