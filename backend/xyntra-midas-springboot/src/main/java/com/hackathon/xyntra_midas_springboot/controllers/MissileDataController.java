package com.hackathon.xyntra_midas_springboot.controllers;


import com.hackathon.xyntra_midas_springboot.model.MissileData;
import com.hackathon.xyntra_midas_springboot.model.Position;
import org.springframework.web.bind.annotation.*;
import org.springframework.http.ResponseEntity;


@RestController
@RequestMapping("/api/missile-data")
public class MissileDataController {
    private MissileData latestMissile;  // Store the latest missile data


    @PostMapping
    public ResponseEntity<String> receiveMissileData(@RequestBody MissileData missile) {
        this.latestMissile = missile;   // Save the latest missile data
        System.out.println("Received");
        return ResponseEntity.ok("Missile data received");
    }
    @GetMapping
    public Position sendMissileData() {
        System.out.println("Send");
        return latestMissile.currentPosition;   // Send the latest missile data to frontend
    }
}

