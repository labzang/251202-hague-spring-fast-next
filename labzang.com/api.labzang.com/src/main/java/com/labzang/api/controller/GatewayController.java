package com.labzang.api.controller;

import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.responses.ApiResponses;
import io.swagger.v3.oas.annotations.tags.Tag;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.time.LocalDateTime;
import java.util.HashMap;
import java.util.Map;

@RestController
@RequestMapping("/api/gateway")
@Tag(name = "Gateway", description = "API Gateway 관리 엔드포인트")
public class GatewayController {

    @Operation(
        summary = "Gateway 상태 확인",
        description = "API Gateway의 현재 상태와 정보를 반환합니다."
    )
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "성공적으로 상태 정보를 반환"),
        @ApiResponse(responseCode = "500", description = "서버 내부 오류")
    })
    @GetMapping("/status")
    public ResponseEntity<Map<String, Object>> getGatewayStatus() {
        Map<String, Object> status = new HashMap<>();
        status.put("service", "Labzang API Gateway");
        status.put("status", "running");
        status.put("timestamp", LocalDateTime.now());
        status.put("version", "1.0.0");
        
        return ResponseEntity.ok(status);
    }

    @Operation(
        summary = "사용 가능한 서비스 목록",
        description = "Gateway를 통해 접근 가능한 마이크로서비스 목록을 반환합니다."
    )
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "성공적으로 서비스 목록을 반환")
    })
    @GetMapping("/services")
    public ResponseEntity<Map<String, Object>> getAvailableServices() {
        Map<String, Object> services = new HashMap<>();
        
        Map<String, Object> transformerService = new HashMap<>();
        transformerService.put("name", "TransformerService");
        transformerService.put("description", "KoELECTRA 기반 한국어 감성분석");
        transformerService.put("path", "/api/transformer/**");
        transformerService.put("port", "9020");
        transformerService.put("docs", "http://localhost:9020/docs");
        
        Map<String, Object> mlService = new HashMap<>();
        mlService.put("name", "MLService");
        mlService.put("description", "머신러닝 및 NLP 서비스");
        mlService.put("path", "/api/ml/**");
        mlService.put("port", "9010");
        
        services.put("transformer", transformerService);
        services.put("ml", mlService);
        services.put("total_services", 2);
        
        return ResponseEntity.ok(services);
    }

    @Operation(
        summary = "Gateway 라우팅 정보",
        description = "현재 설정된 라우팅 규칙 정보를 반환합니다."
    )
    @GetMapping("/routes")
    public ResponseEntity<Map<String, Object>> getRoutes() {
        Map<String, Object> routes = new HashMap<>();
        
        Map<String, String> transformerRoute = new HashMap<>();
        transformerRoute.put("path", "/api/transformer/**");
        transformerRoute.put("target", "http://transformerservice:9020");
        transformerRoute.put("description", "KoELECTRA 감성분석 서비스");
        
        Map<String, String> mlRoute = new HashMap<>();
        mlRoute.put("path", "/api/ml/**");
        mlRoute.put("target", "http://mlservice:9010");
        mlRoute.put("description", "머신러닝 서비스");
        
        routes.put("transformer_route", transformerRoute);
        routes.put("ml_route", mlRoute);
        
        return ResponseEntity.ok(routes);
    }
}
