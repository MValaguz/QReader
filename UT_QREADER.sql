CREATE TABLE ut_qreader (
  user_co   VARCHAR2(20)  NOT NULL,
  codic_co  VARCHAR2(1000)
)
/

COMMENT ON TABLE ut_qreader IS 'Tabella temporanea per il passaggio dei dati ricevuti dalla webcam del PC';

COMMENT ON COLUMN ut_qreader.user_co IS 'Utente';
COMMENT ON COLUMN ut_qreader.codic_co IS 'Dato letto dalla webcam (codice a barre o qrcode)';

GRANT DELETE,INSERT,SELECT,UPDATE ON ut_qreader TO smile_role;


CREATE PUBLIC SYNONYM ut_qreader FOR ut_qreader
