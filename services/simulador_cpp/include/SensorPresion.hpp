#pragma once
#include "SensorBase.hpp"

class SensorPresion : public SensorBase {
public:
    SensorPresion();
    std::string getTipo() const override;
    double leerValor() const override;
};
