package com.hackathon.xyntra_midas_springboot.repository;
import com.hackathon.xyntra_midas_springboot.model.User;

import org.springframework.data.jpa.repository.JpaRepository;

public interface UserRepository extends JpaRepository<User, Long> {
    User findByUsername(String username);
}
