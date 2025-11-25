package com.labzang.api.kakao;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.Map;

@RestController
@RequestMapping("/auth/kakao")
public class KakaoController {

    @GetMapping("/callback")
    public ResponseEntity<Map<String, Object>> kakaoCallback(@RequestParam(required = false) String code) {
        Map<String, Object> response = new HashMap<>();
        response.put("success", true);
        response.put("message", "카카오 로그인 성공");
        response.put("token", "mock-jwt-token-" + System.currentTimeMillis());
        response.put("user", Map.of(
                "id", "kakao_user_123",
                "email", "user@example.com",
                "name", "테스트 사용자"));

        return ResponseEntity.ok(response);
    }

    @PostMapping("/login")
    public ResponseEntity<Map<String, Object>> kakaoLogin(@RequestBody(required = false) Map<String, Object> request) {
        System.out.println("😎😎😎😎😎😎 카카오 로그인 진입 " + request);

        Map<String, Object> response = new HashMap<>();
        response.put("success", true);
        response.put("message", "카카오 로그인 성공");
        response.put("token", "mock-jwt-token-" + System.currentTimeMillis());
        response.put("user", Map.of(
                "id", "kakao_user_123",
                "email", "user@example.com",
                "name", "테스트 사용자"));

        return ResponseEntity.status(HttpStatus.OK).body(response);
    }
}
