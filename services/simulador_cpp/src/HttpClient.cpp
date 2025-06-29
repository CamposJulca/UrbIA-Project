#include "HttpClient.hpp"
#include <curl/curl.h>
#include <iostream>

HttpClient::HttpClient(const std::string& token)
    : token(token), url("http://localhost:8080/api/v1/" + token + "/telemetry") {}

bool HttpClient::enviarJson(const std::string& payload) {
    CURL* curl = curl_easy_init();
    if (!curl) {
        std::cerr << "❌ Error: No se pudo inicializar CURL.\n";
        return false;
    }

    struct curl_slist* headers = nullptr;
    headers = curl_slist_append(headers, "Content-Type: application/json");

    curl_easy_setopt(curl, CURLOPT_URL, url.c_str());
    curl_easy_setopt(curl, CURLOPT_POSTFIELDS, payload.c_str());
    curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);
    curl_easy_setopt(curl, CURLOPT_TIMEOUT, 10L);

    CURLcode res = curl_easy_perform(curl);
    if (res != CURLE_OK) {
        std::cerr << "❌ CURL error: " << curl_easy_strerror(res) << std::endl;
        curl_slist_free_all(headers);
        curl_easy_cleanup(curl);
        return false;
    }

    curl_slist_free_all(headers);
    curl_easy_cleanup(curl);
    return true;
}
