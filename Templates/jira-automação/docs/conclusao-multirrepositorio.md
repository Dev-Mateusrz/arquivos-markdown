# Conclusão entre repositórios

[← Sumário](../README.md)

Comentários formam a timeline da entrega; ausência de comentários pendentes não prova ausência de PRs abertos. Este template usa a alternativa do estudo baseada em uma trava explícita no Jira, sem consultar PRs de outros repositórios.

1. Crie um campo de **texto de linha única** ou **seleção única**, por exemplo “Conclusão global”. O valor inicial deve ser vazio ou diferente de `JIRA_VALOR_CONCLUSAO`.
2. Defina quem pode liberar esse campo: responsável pela entrega ou integração central que conheça todos os repositórios e frentes previstas na issue.
3. Libere somente depois de verificar todas as frentes, todos os PRs relacionados e os impedimentos; confirme também as evidências exigidas pelo projeto. Um único repositório segue a mesma regra.
4. Configure um validador na transição final para conferir o valor exato do campo e os bloqueios aplicáveis. Exigir apenas que o campo seja não vazio é insuficiente se ele também puder conter “Pendente”. Restrinja as transições para que não possam regredir um card já avançado.
5. Revogue a liberação quando houver reabertura, nova frente, novo PR ou impedimento. Restrinja a edição do campo segundo os mecanismos disponíveis na instância.

Sem campo configurado, campo ausente, valor vazio ou divergente, o merge é comentado e o card permanece aberto. O script **não** marca o campo como liberado, não deduz conclusão pela categoria do status e não afirma ter verificado PRs de outros repositórios.

Se a liberação ocorrer após o último merge, não haverá outro evento automático neste workflow. Conclua por uma automação central do Jira que valide a entrega, pela transição manual autorizada ou reexecute a run de merge após a liberação. Para o reprocessamento funcionar, o card deve estar Em análise. Se um evento anterior falhou e ele ainda está em Fazendo, reconcilie primeiro a etapa de revisão.

O script relê status/liberação antes do POST para reduzir corridas. Leitura e transição não são uma operação atômica: condições/validadores do Jira continuam sendo a autoridade entre repositórios. A transição inicial deve aceitar apenas as origens iniciais, a de revisão apenas origens iniciais/Fazendo e a final apenas Em análise. Não use transições globais sem condições equivalentes. Se a instância não oferecer validação suficiente, mantenha a conclusão manual até configurar uma alternativa adequada.

Os nomes e valores do campo estão em [Configuração](configuracao.md). Consulte [Operação e validação](operacao-e-validacao.md) para recuperação e reprocessamento.
