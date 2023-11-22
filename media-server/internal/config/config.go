package config

import "github.com/ilyakaznacheev/cleanenv"

type Config struct {
	Env  string `env:"ENV" env-default:"prod"`
	Ip   string `env:"IP" env-default:"0.0.0.0"`
	Port int    `env:"PORT" env-default:"8080"`
}

func New() (*Config, error) {
	cfg := &Config{}

	err := cleanenv.ReadEnv(cfg)
	if err != nil {
		return nil, err
	}

	return cfg, nil
}
