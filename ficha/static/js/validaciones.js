document.addEventListener('DOMContentLoaded', function() {
    var form = document.getElementById('evaluacionForm');
    if (form) {
        form.addEventListener('submit', function(event) {
            var inputs = document.querySelectorAll('input, textarea');
            var valid = true;
            inputs.forEach(function(input) {
                if (input.value.trim() === '') {
                    input.classList.add('is-invalid');
                    valid = false;
                } else {
                    input.classList.remove('is-invalid');
                }
            });
            if (!valid) {
                event.preventDefault();
                alert('Por favor, complete todos los campos.');
            }
        });

        // Establecer la fecha y hora actual en el campo de fecha
        var fechaInput = document.getElementById('id_fecha');
        if (fechaInput) {
            var now = new Date();
            var day = ("0" + now.getDate()).slice(-2);
            var month = ("0" + (now.getMonth() + 1)).slice(-2);
            var today = now.getFullYear() + "-" + (month) + "-" + (day);
            fechaInput.value = today;
        }
    }
});


document.addEventListener('DOMContentLoaded', function() {
    function validateField(value, errorMessage) {
        if (value === "") {
            alert(errorMessage);
            return false;
        }
        return true;
    }

    window.validateSection1 = function(event) {
        var valid = true;

        // Validar campos de la sección 1
        var verificacionLaboral = document.getElementById("respuesta-verificacion-laboral").value;
        var tipoErrorVerificacionLaboral = document.querySelector('select[name="tipo-error-verificacion-laboral"]').value;
        var observacionVerificacion = document.querySelector("input[name='observacion_verfic']").value;

        valid &= validateField(verificacionLaboral, "Por favor, seleccione una opción para Verificación Laboral.");
        if (verificacionLaboral === "error") {
            valid &= validateField(tipoErrorVerificacionLaboral, "Por favor, seleccione un tipo de error para Verificación Laboral.");
            valid &= validateField(observacionVerificacion, "Por favor, indique observaciones para la Verificación Laboral.");
        }

        var estadoSituacion = document.getElementById("respuesta-estado-situacion").value;
        var tipoErrorEstadoSituacion = document.querySelector('select[name="tipo-error-estado-situacion"]').value;
        var observacion_estado = document.querySelector("input[name='observacion_estado']").value;

        valid &= validateField(estadoSituacion, "Por favor, seleccione una opción para Estado de Situación.");
        if (estadoSituacion === "error") {
            valid &= validateField(tipoErrorEstadoSituacion, "Por favor, seleccione un tipo de error para Estado de Situación.");
            valid &= validateField(observacion_estado, "Por favor, indique observaciones para el Estado de Situación.");
        }

        var acreditacionIngresos = document.getElementById("respuesta-acreditacion-ingresos").value;
        var tipoErrorAcreditacionIngresos = document.querySelector('select[name="tipo-error-acreditacion-ingresos"]').value;
        var observacion_acredita = document.querySelector("input[name='observacion_acredita']").value;

        valid &= validateField(acreditacionIngresos, "Por favor, seleccione una opción para Acreditación de Ingresos.");
        if (acreditacionIngresos === "error") {
            valid &= validateField(tipoErrorAcreditacionIngresos, "Por favor, seleccione un tipo de error para Acreditación de Ingresos.");
            valid &= validateField(observacion_acredita, "Por favor, indique observaciones para la Acreditación de Ingresos.");
        }

        if (valid) {
            openTab(event, 'section2');
        }
    }

    window.validateSection2 = function(event) {
        var valid = true;

        // Validar campos de la sección 2
        var atribuciones = document.getElementById("respuesta-atribuciones").value;
        var observacionRevCredito = document.querySelector("input[name='observaciones-revision-credito']").value;
        valid &= validateField(atribuciones, "Por favor, seleccione una opción para Atribuciones.");
        if (atribuciones === "error") {
            valid &= validateField(observacionRevCredito, "Por favor, indique observaciones para las Atribuciones.");
        }

        var contribucionGarantia = document.getElementById("respuesta-contribucion-garantia").value;
        var observacionContri = document.querySelector("input[name='observaciones-contribucion-garantia']").value;
        valid &= validateField(contribucionGarantia, "Por favor, seleccione una opción para la Contribución Garantías y/o Aval.");
        if (contribucionGarantia === "error") {
            valid &= validateField(observacionContri, "Por favor, indique observaciones para la Contribución Garantías y/o Aval.");
        }

        var condicionAprob = document.getElementById("respuesta-condiciones-aprobacion").value;
        var tipoErrorCondicionAprob = document.querySelector('select[name="tipo-error-condiciones-aprobacion"]').value;
        var observacionCondicionAprob = document.querySelector("input[name='observacion_condicion_aprob']").value;
        valid &= validateField(condicionAprob, "Por favor, seleccione una opción para las Condiciones de Aprobación.");
        if (condicionAprob === "error") {
            valid &= validateField(tipoErrorCondicionAprob, "Por favor, seleccione un tipo de error para las Condiciones de Aprobación.");
            valid &= validateField(observacionCondicionAprob, "Por favor, indique observaciones para las Condiciones de Aprobación.");
        }

        var cambioEvaAT = document.getElementById("Cambio_evaAT").value;
        var tipoErrorCambioEva = document.querySelector('select[name="tipo-error-Cambio_evaAT"]').value;
        var observacionCambioEva = document.querySelector("input[name='observacion_cambioEva']").value;
        valid &= validateField(cambioEvaAT, "Por favor, seleccione una opción para los Cambio Resultado Evaluación Automática.");
        if (cambioEvaAT === "error") {
            valid &= validateField(tipoErrorCambioEva, "Por favor, seleccione un tipo de error para los Cambio Resultado Evaluación Automática.");
            valid &= validateField(observacionCambioEva, "Por favor, indique observaciones para los Cambio Resultado Evaluación Automática.");
        }

        var resDeuVincula = document.querySelector('select[name="respuesta-deudas-vinculadas"]').value;
        var observacionResDeudaVincu = document.querySelector("input[name='observacion_res_deuda_vincu']").value;
        valid &= validateField(resDeuVincula, "Por favor, seleccione una opción para las Deudas Vinculadas.");
        if (resDeuVincula === "error") {
            valid &= validateField(observacionResDeudaVincu, "Por favor, indique observaciones para las Deudas Vinculadas.");
        }

        if (valid) {
            openTab(event, 'section3');
        }
    }

    window.validateSection3 = function(event) {
        var valid = true;

        // Validar campos de la sección 3
        var ingresosMensuales = document.querySelector('select[name="respuesta-ingresos-mensuales"]').value;
        var obsIngresosMensuales = document.querySelectorAll("input[name='obs-ingresos-mensuales']");
        valid &= validateField(ingresosMensuales, "Por favor, seleccione una opción para Ingresos Mensuales.");
        if (ingresosMensuales === "error") {
            obsIngresosMensuales.forEach(function(input) {
                if (input.value === "") {
                    alert("Por favor, complete todos los campos de observaciones para Ingresos Mensuales.");
                    valid = false;
                }
            });
        }

        var activo = document.querySelector('select[name="respuesta-activo"]').value;
        var obs_activo = document.querySelectorAll("input[name='obs-activo']");
        valid &= validateField(activo, "Por favor, seleccione una opción para el parámetro Activo.");
        if (activo === "error") {
            obs_activo.forEach(function(input) {
                if (input.value === "") {
                    alert("Por favor, complete todos los campos de observaciones para el parámetro Activo.");
                    valid = false;
                }
            });
        }

        var dividendos = document.querySelector('select[name="respuesta-dividendo-gasto-vivienda"]').value;
        var obs_dividendos = document.querySelectorAll("input[name='obs-dividendos']");
        valid &= validateField(dividendos, "Por favor, seleccione una opción para el parámetro Dividendos.");
        if (dividendos === "error") {
            obs_dividendos.forEach(function(input) {
                if (input.value === "") {
                    alert("Por favor, complete todos los campos de observaciones para el parámetro Dividendos.");
                    valid = false;
                }
            });
        }

        var arriendos_pagados = document.querySelector('select[name="arriendos_pagados"]').value;
        var obs_arriendos_pagados = document.querySelectorAll("input[name='obs_arriendos_pagados']");
        valid &= validateField(arriendos_pagados, "Por favor, seleccione una opción para el parámetro Arriendos Pagados.");
        if (arriendos_pagados === "error") {
            obs_arriendos_pagados.forEach(function(input) {
                if (input.value === "") {
                    alert("Por favor, complete todos los campos de observaciones para el parámetro Arriendos Pagados.");
                    valid = false;
                }
            });
        }

        var cuotaPrestaEmpleador = document.querySelector('select[name="Cuota_presta_empleador"]').value;
        var obs_presta_empleador = document.querySelectorAll("input[name='obs_presta_empleador']");
        valid &= validateField(cuotaPrestaEmpleador, "Por favor, seleccione una opción para el parámetro Cuota Préstamo Empleador y/o CCAF.");
        if (cuotaPrestaEmpleador === "error") {
            obs_presta_empleador.forEach(function(input) {
                if (input.value === "") {
                    alert("Por favor, complete todos los campos de observaciones para el parámetro Cuota Préstamo Empleador y/o CCAF.");
                    valid = false;
                }
            });
        }

        var reestructurarRenegociado = document.querySelector('select[name="Reestructurar_renegociado"]').value;
        var obs_Reestructurar_renegociado = document.querySelectorAll("input[name='obs_Reestructurar_renegociado']");
        valid &= validateField(reestructurarRenegociado, "Por favor, seleccione una opción para el parámetro Monto a Restructurar Renegociado.");
        if (reestructurarRenegociado === "error") {
            obs_Reestructurar_renegociado.forEach(function(input) {
                if (input.value === "") {
                    alert("Por favor, complete todos los campos de observaciones para el parámetro Monto a Restructurar Renegociado.");
                    valid = false;
                }
            });
        }

        var cuotaBancoCP = document.querySelector('select[name="Cuota_banco_CP"]').value;
        var obs_Cuota_banco_CP = document.querySelectorAll("input[name='obs_Cuota_banco_CP']");
        valid &= validateField(cuotaBancoCP, "Por favor, seleccione una opción para el parámetro Cuota Banco CP.");
        if (cuotaBancoCP === "error") {
            obs_Cuota_banco_CP.forEach(function(input) {
                if (input.value === "") {
                    alert("Por favor, complete todos los campos de observaciones para el parámetro Cuota Banco CP.");
                    valid = false;
                }
            });
        }

        var cuotaCompraOOII = document.querySelector('select[name="Cuota_compra_OOII"]').value;
        var obs_Cuota_compra_OOII = document.querySelectorAll("input[name='obs_Cuota_compra_OOII']");
        valid &= validateField(cuotaCompraOOII, "Por favor, seleccione una opción para el parámetro Cuota Compra OOII.");
        if (cuotaCompraOOII === "error") {
            obs_Cuota_compra_OOII.forEach(function(input) {
                if (input.value === "") {
                    alert("Por favor, complete todos los campos de observaciones para el parámetro Cuota Compra OOII.");
                    valid = false;
                }
            });
        }

        var montoCompraBancoLP = document.querySelector('select[name="Monto_compra_bancoLP"]').value;
        var obs_Monto_compra_bancoLP = document.querySelectorAll("input[name='obs_Monto_compra_bancoLP']");
        valid &= validateField(montoCompraBancoLP, "Por favor, seleccione una opción para el parámetro Monto Compra Banco LP.");
        if (montoCompraBancoLP === "error") {
            obs_Monto_compra_bancoLP.forEach(function(input) {
                if (input.value === "") {
                    alert("Por favor, complete todos los campos de observaciones para el parámetro Monto Compra Banco LP.");
                    valid = false;
                }
            });
        }

        var montoCompraBancoCP = document.querySelector('select[name="Monto_compra_bancoCP"]').value;
        var obs_Monto_compra_bancoCP = document.querySelectorAll("input[name='obs_Monto_compra_bancoCP']");
        valid &= validateField(montoCompraBancoCP, "Por favor, seleccione una opción para el parámetro Monto Compra Banco CP.");
        if (montoCompraBancoCP === "error") {
            obs_Monto_compra_bancoCP.forEach(function(input) {
                if (input.value === "") {
                    alert("Por favor, complete todos los campos de observaciones para el parámetro Monto Compra Banco CP.");
                    valid = false;
                }
            });
        }

        var montoCompraOOII = document.querySelector('select[name="Monto_compra_OOII"]').value;
        var obs_Monto_compra_OOII = document.querySelectorAll("input[name='obs_Monto_compra_OOII']");
        valid &= validateField(montoCompraOOII, "Por favor, seleccione una opción para el parámetro Monto Compra OOII.");
        if (montoCompraOOII === "error") {
            obs_Monto_compra_OOII.forEach(function(input) {
                if (input.value === "") {
                    alert("Por favor, complete todos los campos de observaciones para el parámetro Monto Compra OOII.");
                    valid = false;
                }
            });
        }

        var montoCompraSBIF = document.querySelector('select[name="Monto_compraSBIF"]').value;
        var obs_Monto_compraSBIF = document.querySelectorAll("input[name='obs_Monto_compraSBIF']");
        valid &= validateField(montoCompraSBIF, "Por favor, seleccione una opción para el parámetro Monto Compra SBIF.");
        if (montoCompraSBIF === "error") {
            obs_Monto_compraSBIF.forEach(function(input) {
                if (input.value === "") {
                    alert("Por favor, complete todos los campos de observaciones para el parámetro Monto Compra SBIF.");
                    valid = false;
                }
            });
        }

        if (valid) {
            openTab(event, 'section4');
        }
    }
        window.validateSection4 = function(event) {
            var valid = true;
    
            // Validar campos de la sección 4
            var actividad = document.querySelector('select[name="Actividad"]').value;
            var obsActividad = document.querySelectorAll("input[name='obs_Actividad']");
            valid &= validateField(actividad, "Por favor, seleccione una opción para el parámetro Actividad.");
            if (actividad === "error") {
                obsActividad.forEach(function(input) {
                    if (input.value === "") {
                        alert("Por favor, complete todos los campos de observaciones para el parámetro Actividad.");
                        valid = false;
                    }
                });
            }
    
            var direccionParticular = document.querySelector('select[name="Dirección_Particular"]').value;
            var obsDireccionPart = document.querySelectorAll("input[name='obs_Dirección_Part']");
            valid &= validateField(direccionParticular, "Por favor, seleccione una opción para el parámetro Dirección Particular.");
            if (direccionParticular === "error") {
                obsDireccionPart.forEach(function(input) {
                    if (input.value === "") {
                        alert("Por favor, complete todos los campos de observaciones para el parámetro Dirección Particular.");
                        valid = false;
                    }
                });
            }
    
            var universidad = document.querySelector('select[name="Universidad"]').value;
            var obsUniversidad = document.querySelectorAll("input[name='obs_Universidad']");
            valid &= validateField(universidad, "Por favor, seleccione una opción para el parámetro Universidad.");
            if (universidad === "error") {
                obsUniversidad.forEach(function(input) {
                    if (input.value === "") {
                        alert("Por favor, complete todos los campos de observaciones para el parámetro Universidad.");
                        valid = false;
                    }
                });
            }
    
            var fechaIngEmpleo = document.querySelector('select[name="Fecha_ing_empleo"]').value;
            var obsFechaIngEmpleo = document.querySelectorAll("input[name='obs_Fecha_ing_empleo']");
            valid &= validateField(fechaIngEmpleo, "Por favor, seleccione una opción para el parámetro Fecha de Ingreso Empleo.");
            if (fechaIngEmpleo === "error") {
                obsFechaIngEmpleo.forEach(function(input) {
                    if (input.value === "") {
                        alert("Por favor, complete todos los campos de observaciones para el parámetro Fecha de Ingreso Empleo.");
                        valid = false;
                    }
                });
            }
    
            var nivelEducacional = document.querySelector('select[name="Nivel_educacional"]').value;
            var obsNivelEducacional = document.querySelectorAll("input[name='obs_Nivel_educacional']");
            valid &= validateField(nivelEducacional, "Por favor, seleccione una opción para el parámetro Nivel Educacional.");
            if (nivelEducacional === "error") {
                obsNivelEducacional.forEach(function(input) {
                    if (input.value === "") {
                        alert("Por favor, complete todos los campos de observaciones para el parámetro Nivel Educacional.");
                        valid = false;
                    }
                });
            }
    
            var nacionalidad = document.querySelector('select[name="Nacionalidad"]').value;
            var obsNacionalidad = document.querySelectorAll("input[name='obs_Nacionalidad']");
            valid &= validateField(nacionalidad, "Por favor, seleccione una opción para el parámetro Nacionalidad.");
            if (nacionalidad === "error") {
                obsNacionalidad.forEach(function(input) {
                    if (input.value === "") {
                        alert("Por favor, complete todos los campos de observaciones para el parámetro Nacionalidad.");
                        valid = false;
                    }
                });
            }
    
            var tipoContrato = document.querySelector('select[name="TipoContrato"]').value;
            var obsTipoContrato = document.querySelectorAll("input[name='obs_TipoContrato']");
            valid &= validateField(tipoContrato, "Por favor, seleccione una opción para el parámetro Tipo de Contrato.");
            if (tipoContrato === "error") {
                obsTipoContrato.forEach(function(input) {
                    if (input.value === "") {
                        alert("Por favor, complete todos los campos de observaciones para el parámetro Tipo de Contrato.");
                        valid = false;
                    }
                });
            }
    
            var tipoRenta = document.querySelector('select[name="TipoRenta"]').value;
            var obsTipoRenta = document.querySelectorAll("input[name='obs_TipoRenta']");
            valid &= validateField(tipoRenta, "Por favor, seleccione una opción para el parámetro Tipo de Renta.");
            if (tipoRenta === "error") {
                obsTipoRenta.forEach(function(input) {
                    if (input.value === "") {
                        alert("Por favor, complete todos los campos de observaciones para el parámetro Tipo de Renta.");
                        valid = false;
                    }
                });
            }
    
            var carreraSemestre = document.querySelector('select[name="Carrera_semestre"]').value;
            var obsCarreraSemestre = document.querySelectorAll("input[name='obs_Carrera_semestre']");
            valid &= validateField(carreraSemestre, "Por favor, seleccione una opción para el parámetro Carrera/Semestre.");
            if (carreraSemestre === "error") {
                obsCarreraSemestre.forEach(function(input) {
                    if (input.value === "") {
                        alert("Por favor, complete todos los campos de observaciones para el parámetro Carrera/Semestre.");
                        valid = false;
                    }
                });
            }
    
            var profesion = document.querySelector('select[name="Profesion"]').value;
            var obsProfesion = document.querySelectorAll("input[name='obs_Profesion']");
            valid &= validateField(profesion, "Por favor, seleccione una opción para el parámetro Profesión.");
            if (profesion === "error") {
                obsProfesion.forEach(function(input) {
                    if (input.value === "") {
                        alert("Por favor, complete todos los campos de observaciones para el parámetro Profesión.");
                        valid = false;
                    }
                });
            }
    
            var estadoCivil = document.querySelector('select[name="Estado_civil"]').value;
            var obsEstadoCivil = document.querySelectorAll("input[name='obs_Estado_civil']");
            valid &= validateField(estadoCivil, "Por favor, seleccione una opción para el parámetro Estado Civil.");
            if (estadoCivil === "error") {
                obsEstadoCivil.forEach(function(input) {
                    if (input.value === "") {
                        alert("Por favor, complete todos los campos de observaciones para el parámetro Estado Civil.");
                        valid = false;
                    }
                });
            }
    
            if (valid) {
                openTab(event, 'section5');
            }
        }

        window.openTab= function(event, tabName) {
            // Obtener todas las pestañas
            var tablinks = document.getElementsByClassName("tablinks");
            for (var i = 0; i < tablinks.length; i++) {
                tablinks[i].className = tablinks[i].className.replace(" active", "");
            }
    
            // Mostrar la pestaña seleccionada
            document.getElementById(tabName).style.display = "block";
    
            // Añadir la clase "active" al botón de la pestaña seleccionada
            event.currentTarget.className += " active";
        }

        window.goBack = function(previousSection) {
        // Mostrar la sección anterior
        document.getElementById(previousSection).style.display = "block";
    }
});