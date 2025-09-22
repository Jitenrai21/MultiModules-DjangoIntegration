from django.core.management.base import BaseCommand
from MultiModuleApp.services.llm_service import llm_service, LLMServiceError

class Command(BaseCommand):
    help = 'Test LLM service connectivity and response quality'

    def add_arguments(self, parser):
        parser.add_argument(
            '--prompt',
            type=str,
            default='Hello, who are you?',
            help='Test prompt to send to the LLM'
        )
        parser.add_argument(
            '--persona',
            type=str,
            default='Isaac Newton',
            help='Persona to test with'
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Testing LLM Service...'))
        
        # Check provider status
        status = llm_service.get_provider_status()
        self.stdout.write('\nProvider Status:')
        for provider, info in status.items():
            status_color = self.style.SUCCESS if info['available'] else self.style.ERROR
            self.stdout.write(f"  {provider}: {status_color(info['available'])} ({info['type']})")
        
        # Test basic prompt
        try:
            prompt = options['prompt']
            self.stdout.write(f'\nTesting with prompt: "{prompt}"')
            
            response = llm_service.generate_response(prompt, session_id="test_session")
            
            self.stdout.write(self.style.SUCCESS('\n✅ Response received:'))
            self.stdout.write(f'"{response}"')
            
        except LLMServiceError as e:
            self.stdout.write(self.style.ERROR(f'\n❌ LLM Service Error: {e}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'\n❌ Unexpected Error: {e}'))
        
        # Test persona-based prompt
        persona = options['persona']
        try:
            persona_prompt = f"""You are {persona}, a Mathematician and physicist. Please respond in their style and voice, as if you are them. 
However, always remember: 
- You should **never** talk about harmful, inappropriate, or sensitive topics such as violence, hate, abuse, or any content not suitable for children.
- If a user asks about these topics, redirect the conversation to something more positive and educational.
- Always maintain a friendly, respectful, and child-appropriate tone.
- If the user uses inappropriate language or asks about sensitive subjects, kindly ask them to focus on something else, and gently remind them to be respectful.

Stay positive and educational in all your responses.

User: {prompt}"""
            
            self.stdout.write(f'\nTesting persona "{persona}" with same prompt...')
            
            persona_response = llm_service.generate_response(
                persona_prompt, 
                session_id="test_persona_session"
            )
            
            self.stdout.write(self.style.SUCCESS('\n✅ Persona response received:'))
            self.stdout.write(f'"{persona_response}"')
            
        except LLMServiceError as e:
            self.stdout.write(self.style.ERROR(f'\n❌ Persona Test Error: {e}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'\n❌ Unexpected Persona Error: {e}'))
        
        self.stdout.write(self.style.SUCCESS('\n🎉 LLM Service test completed!'))