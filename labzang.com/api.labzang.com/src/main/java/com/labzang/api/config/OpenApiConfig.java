package com.labzang.api.config;

import io.swagger.v3.oas.models.OpenAPI;
import io.swagger.v3.oas.models.info.Contact;
import io.swagger.v3.oas.models.info.Info;
import io.swagger.v3.oas.models.info.License;
import io.swagger.v3.oas.models.servers.Server;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import java.util.List;

@Configuration
public class OpenApiConfig {

    @Bean
    public OpenAPI customOpenAPI() {
        return new OpenAPI()
                .info(new Info()
                        .title("Labzang API Gateway")
                        .description("""
                            🚀 **Labzang.com 마이크로서비스 API Gateway**
                            
                            ## 주요 기능
                            - 🔄 **마이크로서비스 라우팅**: 각 서비스로 요청 전달
                            - 🤖 **AI 서비스 통합**: ML/NLP/감성분석 서비스
                            - 🔐 **인증 및 권한**: 통합 인증 관리
                            - 📊 **모니터링**: 서비스 상태 및 성능 모니터링
                            
                            ## 사용 가능한 서비스
                            - **TransformerService**: KoELECTRA 감성분석 (`/api/transformer/**`)
                            - **MLService**: 머신러닝 및 NLP (`/api/ml/**`)
                            
                            ## 직접 접근 URL
                            - **TransformerService Docs**: [http://localhost:9020/docs](http://localhost:9020/docs)
                            - **MLService**: [http://localhost:9010](http://localhost:9010)
                            
                            ## 사용 예시
                            ```bash
                            # Gateway를 통한 감성분석
                            POST http://localhost:8080/api/transformer/koelectra/analyze
                            {
                                "text": "이 영화는 정말 재미있어요!"
                            }
                            ```
                            """)
                        .version("1.0.0")
                        .contact(new Contact()
                                .name("Labzang AI Team")
                                .url("https://labzang.com")
                                .email("contact@labzang.com"))
                        .license(new License()
                                .name("MIT License")
                                .url("https://opensource.org/licenses/MIT")))
                .servers(List.of(
                        new Server()
                                .url("http://localhost:8080")
                                .description("로컬 개발 서버"),
                        new Server()
                                .url("https://api.labzang.com")
                                .description("프로덕션 서버")
                ));
    }
}
