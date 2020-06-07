from deeppavlov import build_model, configs

model = build_model(configs. squad. squad, download=True)
print(model(['DeepPavlov is library for NLP and dialog systems. '], ['What is DeepPavlov?']))