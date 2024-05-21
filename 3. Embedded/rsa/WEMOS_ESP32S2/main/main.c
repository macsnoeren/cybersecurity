#include <stdio.h>
#include <string.h>

#include <freertos/FreeRTOS.h>
#include <freertos/task.h>

#include <driver/gpio.h>
#include <driver/uart.h>
#include <nvs_flash.h>

#include <mbedtls/entropy.h>
#include <mbedtls/ctr_drbg.h>
#include <mbedtls/pk.h>
#include <mbedtls/base64.h>

const TickType_t xDelay = 500 / portTICK_PERIOD_MS;

const char* public_key_server_2048 =
"-----BEGIN PUBLIC KEY-----\n"
"MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAukDSvCZjw4Rj+TEfa+5+\n"
"Np1sKMkgbh+wJDmy4wR8yn0LwWIYlb9GzjDcT22G39XNjMXHVVJ/Czk/lji24O2R\n"
"OGrkInm3DAK7a/mXh/X2xwZSv0CFlOBclkv3wf0fM2fC83KO2VgZkbPdYn+btPbH\n"
"Y4pzewB+UuqjZmnVXodAe/skcZCGtB2JaY/9UVurdefIzwKHWDbFAJUzfcwW3oDr\n"
"8CWW9idpJ4BDp2oANhwgJQGwbREC4iLLJtFlAx5wKrDyh6c8RDcQEcpqZUe9cVmN\n"
"5NLsl1dCcLoXeZcgJdgDe2M0dyrFQvj/jrqn/nl7ancoQ+L7MkrSHTN+1M0v4syc\n"
"YwIDAQAB\n"
"-----END PUBLIC KEY-----\n";

const char* public_key_server_4096 =
"-----BEGIN PUBLIC KEY-----\n"
"MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEAycv/gcFMKJJThC2oU/rB\n"
"A14AB/nUxPIs5KVA6Z7ZBjp1rNB2JWATB4ghXvA9MeynqG6TJ/U/0yeZJlbxfKF9\n"
"zYsYL4+u/fdxEq7plMsKEYPtjQ3T1JhcnTYAoX4wLgN0nEjaZoW/m6NuIf5WbN3q\n"
"WF1sxvohEew1gLBLR+/BMkQxvykhvaIRvvvIBI2YJin8OKe+EK7bbkuZ0AIoxymP\n"
"lDJLm5DuTtlVLu05dMiaovZDuZP+9utNpxGJSEVZKW54fr3yrkMd3DsR4N5Gixvh\n"
"nPv5JWlWrMHItqM6KImTUfIFBnGRbByghjSy57klNIP+FgwrHqP6pL7hzOcmrjF3\n"
"OfBmaKPAbh++PCuYOtA3xjY/AFKZ9QnAm+lRcmmw6mnKcyAzQiql1crnkf+ttLNS\n"
"zaoH13DQEYqVDId94Vug0lyDchcI5CX7CaA1FKC9OshFtOTNvz7sxWVWWwbNV7Qx\n"
"8rcs15m6Gvp4nYzaDS2FsYPeDp1TZtGuyR3OMwjl/hoI24R79LCXmiZJf4YXZOg9\n"
"51KLv6K7mRV9LvqS2GinJJ+ViElCts2M8JHcjbXXLkzFxWzHh16VFNE8iUCx6AOj\n"
"NlhBpzEVOnHLMr+VK6Q2/5UbluqNKyOMKc06BNJk/bu0H/0jAoc8J26Vf0OEnc0q\n"
"1Mz3YwexQmwbstlCdp7k+/kCAwEAAQ==\n"
"-----END PUBLIC KEY-----\n";

void app_main(void)
{
    nvs_flash_init();

    gpio_set_direction(GPIO_NUM_15, GPIO_MODE_OUTPUT);
    uart_set_baudrate(UART_NUM_0, 115200);

    gpio_set_level(GPIO_NUM_15, 1);
    vTaskDelay( xDelay );
    gpio_set_level(GPIO_NUM_15, 0);
    vTaskDelay( xDelay );

    int ret = 0;
    mbedtls_entropy_context entropy;
    mbedtls_entropy_init(&entropy);

    mbedtls_ctr_drbg_context ctr_drbg;
    mbedtls_ctr_drbg_init(&ctr_drbg);

    char *pers="anything"; 
    mbedtls_ctr_drbg_seed(&ctr_drbg, mbedtls_entropy_func, &entropy,(unsigned char *) pers, strlen(pers));

    mbedtls_pk_context pk;
    mbedtls_pk_init( &pk );

    ret = mbedtls_pk_parse_public_key(&pk, (const unsigned char*) public_key_server_2048, strlen(public_key_server_2048)+1);
    if ( ret == 0 ) {
        gpio_set_level(GPIO_NUM_15, 1);
    } else {
        for ( int i=0; i > ret; i-- ) {
            gpio_set_level(GPIO_NUM_15, 1);
            vTaskDelay( xDelay );
            gpio_set_level(GPIO_NUM_15, 0);
            vTaskDelay( xDelay );
        }
    }

    unsigned char buf[MBEDTLS_MPI_MAX_SIZE];
    unsigned char data[] = "Dit is de ESP32S2 talking!!\n";
    size_t olen = 0;

    ret = mbedtls_pk_encrypt( &pk, data, strlen((char*) data),
                                    buf, &olen, sizeof(buf),
                                    mbedtls_ctr_drbg_random, &ctr_drbg );
    if ( ret == 0 ) {
        gpio_set_level(GPIO_NUM_15, 1);
    } else {
        for ( int i=0; i > ret; i-- ) {
            gpio_set_level(GPIO_NUM_15, 1);
            vTaskDelay( xDelay );
            gpio_set_level(GPIO_NUM_15, 0);
            vTaskDelay( xDelay );
        }
    }

    size_t olen2 = 0;
    printf("Base64!!\n");
    unsigned char b64[1024] = "";
    ret = mbedtls_base64_encode(b64, sizeof(b64), &olen2, buf, olen);
    if ( ret == 0 ) {
        gpio_set_level(GPIO_NUM_15, 1);
        printf("Result: '%s'\n", b64);
    
    } else if ( ret == MBEDTLS_ERR_BASE64_BUFFER_TOO_SMALL ) {
        printf("Buffer too small!\n");

    } else if ( ret == MBEDTLS_ERR_BASE64_INVALID_CHARACTER ) {
        printf("Invalid characters!\n");
        

    } else {
        printf("base64 ret: %x\n", ret);
        for ( int i=0; i > ret; i-- ) {
            gpio_set_level(GPIO_NUM_15, 1);
            vTaskDelay( xDelay );
            gpio_set_level(GPIO_NUM_15, 0);
            vTaskDelay( xDelay );
        }
    }

/*
    ret = mbedtls_pk_parse_public_key(&pk, (const unsigned char*) public_key_server_4096, strlen(public_key_server_4096)+1);
    if ( ret == 0 ) {
        gpio_set_level(GPIO_NUM_15, 1);
    } else {
        for ( int i=0; i > ret; i-- ) {
            gpio_set_level(GPIO_NUM_15, 1);
            vTaskDelay( xDelay );
            gpio_set_level(GPIO_NUM_15, 0);
            vTaskDelay( xDelay );
        }
    }
*/

    while ( 1 ) {
        vTaskDelay( xDelay );
    }
}
