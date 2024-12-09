<?php
  /**
   * Load JSON file from given path
   * 
   * @param string $file_path
   * @return array|null JSON data as an associative array
   */
  function load_json($file_path): mixed{
    try {
      if (!file_exists(filename: $file_path)) {
        throw new Exception(message: "File not found");
      }

      $json_data = file_get_contents(filename: $file_path);
      $data = json_decode($json_data, associative: true);

      if (json_last_error() !== JSON_ERROR_NONE) {
        throw new Exception(message: "Invalid JSON data");
      }

      return $data;
    } catch (Exception $e) {
      echo "Error: " . $e->getMessage() . PHP_EOL;
      return null;
    }
  }

  /**
   * Format and ecord log of changes made to the leads
   * 
   * 
   * @param array $original
   * @param array $updated
   * @return array Log of changes made to the leads 
   */
  function log_changes($original, $updated): array {
    $changes = [];
    foreach ($updated as $key => $newValue) {
      $oldValue = $original[$key] ?? null;
      if ($oldValue !== $newValue) {
        $changes[] = [
          "field" => $key,
          "from" => $oldValue,
          "to" => $newValue
        ];
      }
    }
    return $changes;
  }


  /**
   * Deduplicate an array of onjects by a given key
   * 
   * @param string $key Key to deduplicate by
   * @param array $data Array of objects to deduplicate
   * @param array $log Log of changes made to the leads
   * @return array Deduplicated array of objects
   */
  function deduplicate_by_key(string $key, array $data, array &$log): array {
    $deduplicated = [];

    foreach ($data as $index => $record) {
      $value = $record[$key];

      if (!isset($deduplicated[$value])) {
        $deduplicated[$value] = ['record' => $record, 'index' => $index];
      } else {
        $current = $deduplicated[$value];
        $currentRecord = $current['record'];
        $currentIndex = $current['index'];

        if (
          $record['entryDate'] > $currentRecord['entryDate'] ||
          ($record['entryDate'] === $currentRecord['entryDate'] && $index > $currentIndex)
        ) {
          $deduplicated[$value] = ['record' => $record, 'index' => $index];

          $log[] = [
          "source" => $currentRecord,
          "updated" => $record,
          "changes" => log_changes(original: $currentRecord, updated: $record),
          ];
        }
      }
    }

    $deduplicated_leads = [];
    foreach ($deduplicated as $updated_record) {
      $deduplicated_leads[] = $updated_record['record'];
    }

    return $deduplicated_leads;
  }

  function deduplicate($data, $keys=['email', '_id']): array {
    $changeLog = [];
    foreach ($keys as $key) {
      $data = deduplicate_by_key(key: $key, data: $data, log: $changeLog);
    }
    return ['leads' => $data, 'changeLog' => $changeLog];
  }


  function main(): void {
    $options = getopt(short_options: "", long_options: ["input_file:", "output_file:"]);
    
    if (!isset($options['input_file']) || !isset($options['output_file'])) {
        echo "Usage: php script.php --input_file=<input_file> --output_file=<output_file>\n";
        exit(1);
    }

    $inputFile = $options['input_file'];
    $outputFile = $options['output_file'];

    $data = load_json(file_path: $inputFile);
    $leads = $data['leads'];

    $result = deduplicate(data: $leads);
    $deduplicatedData = $result['leads'];
    $changeLog = $result['changeLog'];

    file_put_contents(filename: $outputFile, data: json_encode(value: ["leads" => $deduplicatedData, "change_log" => $changeLog], flags: JSON_PRETTY_PRINT));

    echo "Deduplicated data saved to $outputFile\n";
}

  main();
?>