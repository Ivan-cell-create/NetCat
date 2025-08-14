# NetCat

Из по Windows открываю порт для тестов: New-NetFirewallRule -DisplayName "NetCat 5555" -Direction Inbound -LocalPort 5555 -Protocol TCP -Action Allow
