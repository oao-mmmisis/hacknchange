import "package:flutter/material.dart";
import "package:just_audio/just_audio.dart";
import 'package:http/http.dart' as http;
import 'dart:convert';

const String host = "http://localhost";

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: Scaffold(
        appBar: AppBar(
          title: const Text('Audio Streaming'),
        ),
        body: FutureBuilder<ListView>(
          future: getSpaces(),
          builder: (context, snapshot) {
            if (snapshot.connectionState == ConnectionState.waiting) {
              return const CircularProgressIndicator();
            } else if (snapshot.hasError) {
              return Text("${snapshot.error}");
            } else if (snapshot.hasData) {
              return snapshot.data!;
            } else {
              return const Text('No data available');
            }
          },
        ),
        floatingActionButton: FloatingActionButton(
          onPressed: () {
            addSpace();
          },
          child: const Icon(Icons.add),
        ),
      ),
    );
  }

}

Future<void> addSpace() async {
  final url = Uri.parse('$host/space/add');
  final headers = {
    'accept': 'application/json',
    'Content-Type': 'application/json',
  };

  final data = {
    "name": "string",
    "private": true,
    "description": "string",
  };

  final response = await http.post(
    url,
    headers: headers,
    body: jsonEncode(data),
  );

  if (response.statusCode == 200) {
    print('Request successful');
    print('Response: ${response.body}');
  } else {
    print('Request failed with status: ${response.statusCode}');
    print('Response: ${response.body}');
  }
}

Future<ListView> getSpaces() async {
  final url = Uri.parse('$host/spaces');
  final headers = {
    'accept': 'application/json',
    'Content-Type': 'application/json',
  };

  final response = await http.get(
    url,
    headers: headers,
  );

  if (response.statusCode == 200) {
    print('Request successful');
    print('Response: ${response.body}');
  } else {
    print('Request failed with status: ${response.statusCode}');
    print('Response: ${response.body}');
  }


  List<dynamic> data = jsonDecode(response.body)['data'];

  return ListView(
    children: data.map((item) {
      return ListTile(
        title: Text(item['name']),
        subtitle: Text(item['description']),
        leading: Icon(item['private'] ? Icons.lock : Icons.lock_open),
        onTap: () {
          playAudio(item['id']);
        }
      );
    }).toList(),
  );
}

void playAudio(int spaceId) async {
  await playRequest(spaceId, "dante");
  await Future.delayed(const Duration(seconds: 3));
  
  final player = AudioPlayer();
  await player.setUrl('$host/audio/$spaceId');
  player.play();
}

Future<void> playRequest(int spaceId, String song) async {
  final url = Uri.parse('$host/play');
  final headers = {
    'accept': 'application/json',
    'Content-Type': 'application/json',
  };

  final data = {
    "space_id": spaceId,
    "song": song,
  };

  final response = await http.post(
    url,
    headers: headers,
    body: jsonEncode(data),
  );

  if (response.statusCode == 200) {
    print('Request successful');
    print('Response: ${response.body}');
  } else {
    print('Request failed with status: ${response.statusCode}');
    print('Response: ${response.body}');
  }
}