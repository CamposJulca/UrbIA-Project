#pragma once
#include "SensorBase.hpp"

class SensorRuido : public SensorBase {
public:
    SensorRuido();
    std::string getTipo() const override;
    double leerValor() const override;
};
