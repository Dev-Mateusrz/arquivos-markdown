# Operação e validação

[← Sumário](../README.md)

## Best-effort e recuperação

- Branch fora da convenção, prefixo não autorizado ou secrets ausentes: sair com sucesso sem chamar o Jira.
- Falha de rede, timeout, HTTP ou JSON: registrar aviso sem expor a resposta e sair com sucesso; tentar comentar o evento se a transição falhar.
- O job tem `continue-on-error: true` como proteção adicional para erros do runner/checkout. Não o configure como check obrigatório nem condicione deploy à sua execução.
- Push de atualização não aloca runner para este job. O GitHub ainda pode criar uma run ignorada: a condição `created` é avaliada no job, não é um filtro nativo do gatilho `push`.
- Forks externos são ignorados antes do checkout. Não substitua este fluxo por `pull_request_target` executando código do PR para obter secrets.
- Não há retentativas automáticas de escritas: um timeout pode ocorrer depois de o Jira efetivar a operação. Confira a issue antes de reexecutar.
- O status já atingido impede repetir a transição, mas comentários podem se repetir em reexecuções. As URLs da run/PR permitem identificar esses registros.
- Best-effort exige acompanhamento dos avisos e reconciliação quando necessário; ele não garante entrega eventual dos eventos.

## Verificação local

Na raiz deste conjunto (`Templates/jira-automação`, um nível acima de `docs`), execute:

```shell
python -B -m unittest discover -s arquivos -p test_jira.py -v
```

Os testes simulam a API e não usam credenciais reais. Depois de adaptar, valide o YAML substituído e exercite os eventos com uma issue de teste no workflow real, incluindo duas frentes e uma tentativa de conclusão sem liberação.

O arquivo [test_jira.py](../arquivos/test_jira.py) pertence à validação deste conjunto e não precisa ser copiado para o projeto consumidor. Antes da verificação real, siga [Instalação](instalacao.md) e [Configuração](configuracao.md).
