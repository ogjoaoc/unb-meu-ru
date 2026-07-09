CREATE OR REPLACE FUNCTION fn_atualiza_nota_media_cardapio()
RETURNS TRIGGER AS $$
DECLARE
    v_id_cardapio INT;
BEGIN
    IF TG_OP = 'DELETE' THEN
        v_id_cardapio := OLD.ID_Cardapio;
    ELSE
        v_id_cardapio := NEW.ID_Cardapio;
    END IF;

    UPDATE Cardapio
    SET Nota_Media = COALESCE(
        (SELECT ROUND(AVG(Nota), 2) FROM Feedback WHERE ID_Cardapio = v_id_cardapio), 
        0.00
    )
    WHERE ID_Cardapio = v_id_cardapio;

    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER tg_atualiza_nota_media
AFTER INSERT OR UPDATE OR DELETE ON Feedback
FOR EACH ROW
EXECUTE FUNCTION fn_atualiza_nota_media_cardapio();