# Orac Med 🩺

Projeto desenvolvido para digitalizar e automatizar processos de gestão de atendimentos, clientes e exames, reduzindo o uso de papel e agilizando tarefas administrativas.  

Resumo rápido: sistema web em Python, arquitetura em camadas (Model / Repository / Service / Routes), autenticação mínima, integração opcional com Google Drive e envio de e‑mail.



## ⚙️ Resumo Funcional
- Cadastro
  - Clientes: formulário de cadastro no módulo de clientes. Campos essenciais (nome, documento, contato). Validação básica no front/back.
  - Usuários: cadastro de conta com nível de acesso. Senha armazenada com hash.
  - Exames: registrar tipos de exames, informações e arquivos associados.
  - Atendimentos: vínculo cliente ↔ exame ↔ usuário, data/hora, observações.
- Listagens
  - Páginas de listagem para clientes, exames e atendimentos com paginação.
  - Filtros por data, cliente e tipo de exame.
- Inserção e Remoção
  - Inserção via formulários nas páginas correspondentes; validações server-side.
  - Remoção com confirmação. 
- Relatórios
  - Geração de relatórios por período, cliente ou tipo de exame (XLSX ou TXT).
  - Relatórios pensados para reduzir impressões e automatizar envio de resultados aos responsáveis.
- Segurança e Acesso
  - Autenticação de usuários e proteção de rotas administrativas.
  - Senhas com hash.
  - Proteção básica contra acesso não autorizado.


## 🧭 Arquitetura e escolhas técnicas
- Linguagem: Python e uso mínimo de bibliotecas externas (apenas para web e banco de dados).
- OOP: separação em Model / Repository / Service / Routes — facilita testes, manutenção e escalabilidade.
- Sustentabilidade: redução do uso de papel, automação de relatórios e comunicação automatizada (impacto ambiental e operacional).


## 🔐 Segurança
- Autenticação mínima implementada.
- Senhas nunca salvas em texto puro.
- Credenciais externas (Google) isoladas fora do repositório (.env + credentials.json).


## ♻️ Impacto social
Solução criada para diminuir impacto ecológico e aumentar eficiência no trabalho — deslocando tarefas administrativas repetitivas para automação, liberando profissionais para atividades de maior valor (empatia, pensamento crítico, atendimento humanizado). Alinha‑se com ODS: 4, 8, 9 e 10.


## 👨🏻‍💻 Autor
 [@RafaelCostrov](https://github.com/RafaelCostrov)
