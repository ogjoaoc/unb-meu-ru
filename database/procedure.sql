CREATE OR REPLACE PROCEDURE pr_realizar_recarga(
    p_matricula INT,
    p_valor DECIMAL(10,2)
)
LANGUAGE plpgsql
AS $$
BEGIN
    -- IF p_valor <= 0 THEN
    --     RAISE EXCEPTION 'valor da recarga deve ser maior que zero';
    -- END IF;

    INSERT INTO Transacao (valor, data_hora, matricula)
    VALUES (p_valor, CURRENT_TIMESTAMP, p_matricula);

    UPDATE Estudante
    SET saldo_ru = saldo_ru + p_valor
    WHERE matricula = p_matricula;
END;
$$;