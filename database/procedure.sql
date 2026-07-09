CREATE OR REPLACE PROCEDURE pr_realizar_recarga(
    p_matricula INT,
    p_valor DECIMAL(10,2)
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_id_transacao INT;
BEGIN
    IF p_valor <= 0 THEN
        RAISE EXCEPTION 'O valor da recarga deve ser maior que zero.';
    END IF;

    v_id_transacao := FLOOR(RANDOM() * (999999 - 100000 + 1) + 100000);

    INSERT INTO Transacao (id_transacao, valor, data_hora, matricula)
    VALUES (v_id_transacao, p_valor, CURRENT_TIMESTAMP, p_matricula);

    UPDATE Estudante
    SET saldo_ru = saldo_ru + p_valor
    WHERE matricula = p_matricula;
END;
$$;
