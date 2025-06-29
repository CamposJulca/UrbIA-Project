#include <iostream>
#include <thread>
#include <chrono>
#include <vector>
#include <memory>
#include <cstdlib>
#include <ctime>
#include <nlohmann/json.hpp>

#include "SensorCO2.hpp"
#include "SensorTemperatura.hpp"
#include "SensorHumedad.hpp"
#include "SensorPresion.hpp"
#include "SensorLuz.hpp"
#include "SensorRuido.hpp"
#include "HttpClient.hpp"
#include "EnvLoader.hpp"
#include "Logger.hpp"

using json = nlohmann::json;

int main() {
    std::srand(static_cast<unsigned int>(std::time(nullptr))); // Semilla aleatoria

    std::string token = getEnvVar("THINGSBOARD_TOKEN");
    if (token.empty()) {
        std::cerr << "❌ Token no definido en .env. Abortando.\n";
        Logger::log("❌ Token no definido en .env. Abortando.");
        return 1;
    }

    HttpClient client(token);

    std::vector<std::shared_ptr<SensorBase>> sensores = {
        std::make_shared<SensorCO2>(),
        std::make_shared<SensorTemperatura>(),
        std::make_shared<SensorHumedad>(),
        std::make_shared<SensorPresion>(),
        std::make_shared<SensorLuz>(),
        std::make_shared<SensorRuido>()
    };

    while (true) {
        json payload;
        for (const auto& sensor : sensores) {
            double valor = sensor->leerValor();
            std::string mensaje = "Sensor: " + sensor->getTipo() + ", Valor: " + std::to_string(valor);
            std::cout << "📡 " << mensaje << std::endl;
            Logger::log(mensaje);
            payload[sensor->getTipo()] = valor;
        }

        if (!client.enviarJson(payload.dump())) {
            std::cerr << "❌ Error al enviar datos a ThingsBoard.\n";
            Logger::log("❌ Error al enviar datos a ThingsBoard.");
        } else {
            std::cout << "✅ Datos enviados correctamente.\n";
            Logger::log("✅ Datos enviados correctamente.");
        }

        std::this_thread::sleep_for(std::chrono::seconds(5));
    }

    return 0;
}
