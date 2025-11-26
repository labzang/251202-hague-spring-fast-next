package com.labzang.api.kakao;

import com.labzang.api.kakao.dto.KakaoTokenResponse;
import com.labzang.api.kakao.dto.KakaoUserInfo;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Service;
import org.springframework.util.LinkedMultiValueMap;
import org.springframework.util.MultiValueMap;
import org.springframework.web.reactive.function.BodyInserters;
import org.springframework.web.reactive.function.client.WebClient;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;

@Slf4j
@Service
@RequiredArgsConstructor
public class KakaoService {

    private final KakaoProperties kakaoProperties;
    private final WebClient webClient;

    public KakaoTokenResponse getAccessToken(String code) {
        MultiValueMap<String, String> params = new LinkedMultiValueMap<>();
        params.add("grant_type", "authorization_code");
        params.add("client_id", kakaoProperties.getRestApiKey());
        params.add("redirect_uri", kakaoProperties.getRedirectUri());
        params.add("code", code);

        try {
            KakaoTokenResponse response = webClient.post()
                    .uri(kakaoProperties.getTokenUrl())
                    .header(HttpHeaders.CONTENT_TYPE, MediaType.APPLICATION_FORM_URLENCODED_VALUE)
                    .body(BodyInserters.fromFormData(params))
                    .retrieve()
                    .bodyToMono(KakaoTokenResponse.class)
                    .block();

            log.info("카카오 액세스 토큰 획득 성공");
            return response;
        } catch (Exception e) {
            log.error("카카오 액세스 토큰 획득 실패: {}", e.getMessage(), e);
            throw new RuntimeException("카카오 액세스 토큰 획득 실패", e);
        }
    }

    public KakaoUserInfo getUserInfo(String accessToken) {
        try {
            KakaoUserInfo userInfo = webClient.get()
                    .uri(kakaoProperties.getUserInfoUrl())
                    .header(HttpHeaders.AUTHORIZATION, "Bearer " + accessToken)
                    .retrieve()
                    .bodyToMono(KakaoUserInfo.class)
                    .block();

            log.info("카카오 사용자 정보 획득 성공: {}", userInfo.getId());
            return userInfo;
        } catch (Exception e) {
            log.error("카카오 사용자 정보 획득 실패: {}", e.getMessage(), e);
            throw new RuntimeException("카카오 사용자 정보 획득 실패", e);
        }
    }

    public String getAuthUrl() {
        return kakaoProperties.getAuthUrl();
    }
}
