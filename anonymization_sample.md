# Instructional Guide: Dataset Anonymization Process

This guide explains how to transform a raw dataset containing personally identifiable information (PII) into an anonymized version suitable for research and analysis.

---

## 1. Initial Data Collection

Initially, your dataset consists of identifiable files for 10 participants (e.g., Tom, Jerry, and 8 others):

- 10 Past Transaction Logs: Tom_trans.xls, Jerry_trans.xls, etc.
- 10 Signed Informed Consents: Tom_consent.pdf, Jerry_consent.pdf, etc.
- 1 Demographics File: A master list containing participant info (age, zone, profession, etc.)

---

## 2. Pre-Anonymization View (Raw Data)

### Sample: transactions.xls

| Date       | Heure    | Direction | Contact     | Téléphone | Contenu                                                                                                                              | Type |
| ---------- | -------- | --------- | ----------- | ----------- | ------------------------------------------------------------------------------------------------------------------------------------ | ---- |
| 2025-02-21 | 09:30:07 | Reçu     | OrangeMoney | OrangeMoney | Paiement de SEMBE WOILA en succès par 6995098203. ID transaction: MP250221.0930.C42749, Montant: 200 FCFA, Nouveau solde: 5534 FCFA | SMS  |
| 2025-02-21 | 16:42:28 | Reçu     | OrangeMoney | OrangeMoney | Paiement de SWITCHN réussi par 6995098203 JERRY THE MOUSE. ID transaction: MP250221.1642.C75125, Montant: 160 FCFA                  | SMS  |
| 2025-02-22 | 07:46:51 | Reçu     | OrangeMoney | OrangeMoney | Transfert de 6995098703 JERRY THE MOUSE vers 698016232 BLANCHE NEIGE réussi. ID transaction: MP250222.0746.C35694                   | SMS  |

---

### Sample: Demographics (Raw)

| User            | Age Range | Gender | Profession | Education   | Monthly Income   | Geographic Zone             |
| --------------- | --------- | ------ | ---------- | ----------- | ---------------- | --------------------------- |
| JERRY THE MOUSE | 25–34    | M      | Driver     | Bachelor    | 200,000–500,000 | Urban (Yaoundé, Centre)    |
| TOM THE CAT     | 18–24    | M      | Student    | High School | < 100,000        | Suburban (Douala, Littoral) |

---

## 3. The Anonymization Process

### Step 1: Identification of Sensitive Information

We must locate all PII (Personally Identifiable Information) within the data:

- Participant Names: TOM THE CAT, JERRY THE MOUSE
- Third-Party Names: BLANCHE NEIGE, etc.
- Phone Numbers: 6995098203, 696224574, etc.
- Other Identifiers: Transaction IDs (which can be traced back to accounts)

---

### Step 2: Anonymization Strategy

Apply the following replacement rules:

1. Participant Names → User IDs

   - Example:
     - JERRY THE MOUSE → user0001
     - TOM THE CAT → user0002
2. Other Names → "Mr. X"
3. Phone Numbers → "XXXX"
4. Transaction IDs → "ID_MASKED"

---

## 4. Anonymization Results (Final Data)

### Updated File Structure

- Transaction Logs: user0001.xls, user0002.xls, etc.
- Demographics File: demographic_anonym.xls

---

### Example: Content of user0001.xls

| Date       | Heure    | Contact     | Contenu (anonymized)                                                                                  |
| ---------- | -------- | ----------- | ----------------------------------------------------------------------------------------------------- |
| 2025-02-21 | 09:30:07 | OrangeMoney | Paiement de SWITCHN réussi par XXXX user0001. ID transaction: ID_MASKED, Montant: 150 FCFA           |
| 2025-02-22 | 07:46:51 | OrangeMoney | Transfert de XXXX user0001 vers XXXX Mr. X réussi. ID transaction: ID_MASKED, Montant Net: 1608 FCFA |

---

### Example: demographic_anonym.xls

| User ID  | Age Range | Gender | Profession | Geographic Zone             |
| -------- | --------- | ------ | ---------- | --------------------------- |
| user0001 | 25–34    | M      | Driver     | Urban (Yaoundé, Centre)    |
| user0002 | 18–24    | M      | Student    | Suburban (Douala, Littoral) |
