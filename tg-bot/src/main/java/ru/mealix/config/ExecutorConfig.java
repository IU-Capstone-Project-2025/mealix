package ru.mealix.config;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.scheduling.annotation.EnableAsync;
import org.springframework.scheduling.concurrent.ThreadPoolTaskExecutor;

import java.util.concurrent.Executor;

@Configuration
@EnableAsync
public class ExecutorConfig {

    @Value("${bot.corePoolSize}")
    private int corePoolSize;
    @Value("${bot.maxPoolSize}")
    private int maxPoolSize;
    @Value("${bot.queueCapacity}")
    private int queueCapacity;

    @Bean(name = "botAsyncExecutor")
    public Executor asyncExecutor() {
        ThreadPoolTaskExecutor executor = new ThreadPoolTaskExecutor();
        executor.setCorePoolSize(corePoolSize);
        executor.setMaxPoolSize(maxPoolSize);
        executor.setQueueCapacity(queueCapacity);
        executor.setThreadNamePrefix("BotThread-");
        executor.initialize();
        return executor;
    }

}
