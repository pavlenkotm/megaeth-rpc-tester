{-# LANGUAGE DataKinds           #-}
{-# LANGUAGE NoImplicitPrelude   #-}
{-# LANGUAGE TemplateHaskell     #-}
{-# LANGUAGE ScopedTypeVariables #-}
{-# LANGUAGE TypeApplications    #-}
{-# LANGUAGE TypeFamilies        #-}
{-# LANGUAGE OverloadedStrings   #-}

module PlutusValidator where

import           PlutusTx
import           PlutusTx.Prelude
import qualified Ledger
import           Ledger.Ada                     as Ada
import qualified Ledger.Typed.Scripts           as Scripts
import           Ledger.Value                   (Value)
import qualified Ledger.Value                   as Value
import           Playground.Contract

{-
  Simple Plutus Validator for Cardano

  This validator locks funds that can only be unlocked
  by providing the correct secret number as redeemer.
-}

-- | Datum: the secret number we're looking for
newtype SecretDatum = SecretDatum
    { secretNumber :: Integer
    } deriving Show

PlutusTx.unstableMakeIsData ''SecretDatum

-- | Redeemer: the guess provided to unlock funds
newtype SecretRedeemer = SecretRedeemer
    { guess :: Integer
    } deriving Show

PlutusTx.unstableMakeIsData ''SecretRedeemer

-- | The validator function
{-# INLINABLE mkValidator #-}
mkValidator :: SecretDatum -> SecretRedeemer -> Ledger.ScriptContext -> Bool
mkValidator datum redeemer _ =
    traceIfFalse "Wrong secret!" $ guess redeemer == secretNumber datum

-- | Typed validator
data SecretValidator
instance Scripts.ValidatorTypes SecretValidator where
    type instance DatumType SecretValidator = SecretDatum
    type instance RedeemerType SecretValidator = SecretRedeemer

-- | Compile the validator
typedValidator :: Scripts.TypedValidator SecretValidator
typedValidator = Scripts.mkTypedValidator @SecretValidator
    $$(PlutusTx.compile [|| mkValidator ||])
    $$(PlutusTx.compile [|| wrap ||])
  where
    wrap = Scripts.wrapValidator @SecretDatum @SecretRedeemer

-- | Get the validator
validator :: Ledger.Validator
validator = Scripts.validatorScript typedValidator

-- | Get the validator hash
validatorHash :: Ledger.ValidatorHash
validatorHash = Scripts.validatorHash typedValidator

-- | Get the script address
scrAddress :: Ledger.Address
scrAddress = Ledger.scriptAddress validator

{-
  Example Token Minting Policy

  A simple minting policy that allows minting only once
-}

{-# INLINABLE mkPolicy #-}
mkPolicy :: Ledger.TxOutRef -> () -> Ledger.ScriptContext -> Bool
mkPolicy oref () ctx = traceIfFalse "UTXO not consumed" hasUTxO
  where
    info :: Ledger.TxInfo
    info = Ledger.scriptContextTxInfo ctx

    hasUTxO :: Bool
    hasUTxO = any (\i -> Ledger.txInInfoOutRef i == oref) $ Ledger.txInfoInputs info

-- | Compile the policy
policy :: Ledger.TxOutRef -> Ledger.MintingPolicy
policy oref = Ledger.mkMintingPolicyScript $
    $$(PlutusTx.compile [|| Scripts.wrapMintingPolicy . mkPolicy ||])
    `PlutusTx.applyCode`
    PlutusTx.liftCode oref

-- | Get the currency symbol
curSymbol :: Ledger.TxOutRef -> Ledger.CurrencySymbol
curSymbol = Ledger.scriptCurrencySymbol . policy

{-
  Example Usage Functions
-}

-- | Create a datum with secret
createDatum :: Integer -> SecretDatum
createDatum secret = SecretDatum { secretNumber = secret }

-- | Create a redeemer with guess
createRedeemer :: Integer -> SecretRedeemer
createRedeemer g = SecretRedeemer { guess = g }

-- | Check if a guess is correct
checkGuess :: SecretDatum -> SecretRedeemer -> Bool
checkGuess datum redeemer = guess redeemer == secretNumber datum

{-
  Helper Functions
-}

-- | Convert Ada to Lovelace
adaToLovelace :: Integer -> Value
adaToLovelace ada = Ada.lovelaceValueOf ada

-- | Get minimum Ada value
minAda :: Value
minAda = Ada.lovelaceValueOf 2_000_000  -- 2 ADA minimum

-- | Example: Lock 10 ADA with secret 42
exampleLockValue :: Value
exampleLockValue = Ada.lovelaceValueOf 10_000_000

exampleSecret :: Integer
exampleSecret = 42

exampleDatum :: SecretDatum
exampleDatum = createDatum exampleSecret

exampleCorrectRedeemer :: SecretRedeemer
exampleCorrectRedeemer = createRedeemer 42

exampleWrongRedeemer :: SecretRedeemer
exampleWrongRedeemer = createRedeemer 99
