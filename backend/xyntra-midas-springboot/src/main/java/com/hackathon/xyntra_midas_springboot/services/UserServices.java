package com.hackathon.xyntra_midas_springboot.services;

import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;
import com.hackathon.xyntra_midas_springboot.repository.UserRepository;
import com.hackathon.xyntra_midas_springboot.model.User;


@Component
public class UserServices implements CommandLineRunner {

    private final UserRepository userRepository;

    public UserServices(UserRepository userRepository) {
        this.userRepository = userRepository;
    }

    @Override
    public void run(String... args) throws Exception {
        User user = new User();
        user.setUsername("abdul");
        user.setPassword("secret123");
        user.setEmail("abdul@example.com");
        userRepository.save(user);
    }
}
