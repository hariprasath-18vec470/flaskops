{{- define "flaskops.labels" -}}
app: flaskops
app.kubernetes.io/name: flaskops
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{- define "flaskops.selectorLabels" -}}
app: flaskops
{{- end }}
